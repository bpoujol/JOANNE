# Module to store functions for regression

from sklearn import linear_model
import numpy as np
import xarray as xr
import metpy.calc as mpcalc
from metpy.units import units
import os.path
import joanne

# %% FIT2D function


def fit2d(x, y, u):
    """
    estimate a 2D linear model to calculate u-values from x-y coordinates

    :param x: x coordinates of data points. shape: (...,M)
    :param y: y coordinates of data points. shape: (...,M)
    :param u: data values. shape: (...,M)

    all points along the M dimension are expected to belong to the same model
    all other dimensions are for different models

    :returns: intercept, dudx, dudy. all shapes: (...)
    """
    # to fix nans, do a copy
    u = np.array(u, copy=True)
    # a does not need to be copied as this creates a copy already
    a = np.stack([np.ones_like(x), x, y], axis=-1)

    # for handling missing values, both u and a are set to 0, that way
    # these items don't influence the fit
    invalid = np.isnan(u) | np.isnan(x) | np.isnan(y)
    under_constraint = np.sum(~invalid, axis=-1) < 6
    u[invalid] = 0
    a[invalid] = 0

    a_inv = np.linalg.pinv(a)

    intercept, dudx, dudy = np.einsum("...rm,...m->r...", a_inv, u)

    intercept[under_constraint] = np.nan
    dudx[under_constraint] = np.nan
    dudy[under_constraint] = np.nan

    return intercept, dudx, dudy


def fit2d_xr(x, y, u, sample_dim):

    return xr.apply_ufunc(
        fit2d,
        x,
        y,
        u,
        input_core_dims=[[sample_dim], [sample_dim], [sample_dim]],
        output_core_dims=[(), (), ()],
    )


# %%


def run_regression(circle, parameter):

    """
    Input :
        circle : xarray dataset
                 dataset with sondes of a circle, with dx and dy calculated
                
        parameter : string
                    the parameter on which regression is to be carried out
    
    Output :

        mean_parameter : mean of parameter (intercept)
        m_parameter, c_parameter    : coefficients of regression

    """
    id_u = ~np.isnan(circle.u.values)
    id_v = ~np.isnan(circle.v.values)
    id_q = ~np.isnan(circle.q.values)
    id_x = ~np.isnan(circle.dx.values)
    id_y = ~np.isnan(circle.dy.values)
    id_t = ~np.isnan(circle.ta.values)
    id_p = ~np.isnan(circle.p.values)

    id_quxv = np.logical_and(np.logical_and(id_q, id_u), np.logical_and(id_x, id_v))
    id_ = np.logical_and(np.logical_and(id_t, id_p), id_quxv)

    mean_parameter = np.full(len(circle.alt), np.nan)
    m_parameter = np.full(len(circle.alt), np.nan)
    c_parameter = np.full(len(circle.alt), np.nan)

    Ns = np.full(len(circle.alt), np.nan)  # number of sondes available for regression

    for k in range(len(circle.alt)):
        Ns[k] = id_[:, k].sum()
        if Ns[k] >= 6:
            X_dx = circle["dx"].isel(alt=k).isel(launch_time=id_[:, k]).values
            X_dy = circle["dy"].isel(alt=k).isel(launch_time=id_[:, k]).values

            X = list(zip(X_dx, X_dy))

            Y_parameter = (
                circle[parameter].isel(alt=k).isel(launch_time=id_[:, k]).values
            )

            regr = linear_model.LinearRegression()
            regr.fit(X, Y_parameter)

            mean_parameter[k] = regr.intercept_
            m_parameter[k], c_parameter[k] = regr.coef_
        else:
            Ns[k] = 0

    # if "sondes_regressed" not in circle:
    #     circle["sondes_regressed"] = (["alt"], Ns)

    return (mean_parameter, m_parameter, c_parameter, Ns)


# rename_dict = {
#     "u_wind": "u",
#     "v_wind": "v",
#     "specific_humidity": "q",
#     "temperature": "T",
#     "pressure": "p",
# }


def regress_for_all_parameters(circle, list_of_parameters):

    save_directory = "/Users/geet/Documents/JOANNE/Data/Level_4/Interim_files/"

    file_name = (
        "EUREC4A_JOANNE_Dropsonde-RD41_"
        + str(circle.circle_time.values)
        + "Level_4_v"
        + str(joanne.__version__)
        + ".nc"
    )

    if os.path.exists(save_directory + file_name):

        circle = xr.open_dataset(save_directory + file_name)

    else:

        for par in list_of_parameters:
            (par_mean, par_m, par_c, Ns) = run_regression(circle, par)

            circle[par] = (["alt"], par_mean)
            circle["d" + par + "dx"] = (["alt"], par_m)
            circle["d" + par + "dy"] = (["alt"], par_c)

            if "sondes_regressed" not in list(circle.data_vars):
                circle["sondes_regressed"] = (["alt"], Ns)

        circle.to_netcdf(save_directory + file_name)

    print(f"Finished all parameters ...")

    return circle


def regress_for_all_circles(circles, list_of_parameters):

    # mean = [None] * len(circles)
    # m = [None] * len(circles)
    # c = [None] * len(circles)

    map_iterators = map(
        lambda circle: regress_for_all_parameters(circle, list_of_parameters),
        circles,
        # [list_of_parameters for _ in range(len(circles))],
    )

    for id_, i in enumerate(map_iterators):
        circles[id_] = i
        print(f"{id_+1}/{len(circles)} circles completed ...")

    print(f"Regressed over all circles ...")

    return circles


def get_div_and_vor(circle):

    D = circle.dudx + circle.dvdy
    vor = circle.dvdx - circle.dudy

    circle["D"] = (["circle", "alt"], D)
    circle["vor"] = (["circle", "alt"], vor)

    return print("Finished estimating divergence and vorticity for all circles....")


def get_density_vertical_velocity_and_omega(circle):

    # for circle in circles:
    den_m = [None] * len(circle.launch_time)

    for sounding in range(len(circle.launch_time)):
        mr = mpcalc.mixing_ratio_from_specific_humidity(
            circle.isel(launch_time=sounding).q.values
        )
        den_m[sounding] = mpcalc.density(
            circle.isel(launch_time=sounding).p.values * units.Pa,
            circle.isel(launch_time=sounding).ta.values * units.kelvin,
            mr,
        ).magnitude

    circle["density"] = (["launch_time", "circle", "alt"], den_m)
    circle["mean_density"] = (["circle", "alt"], np.nanmean(den_m, axis=0))

    D = circle.D.values
    mean_den = circle.mean_density

    nan_ids = np.where(np.isnan(D) == True)  # [0]

    w_vel = np.full([len(circle["circle"]), len(circle.alt)], np.nan)
    p_vel = np.full([len(circle["circle"]), len(circle.alt)], np.nan)

    w_vel[:, 0] = 0
    # last = 0

    for cir in range(len(circle["circle"])):
        last = 0
        for m in range(1, len(circle.alt)):

            if (
                len(
                    np.intersect1d(
                        np.where(nan_ids[1] == m)[0], np.where(nan_ids[0] == cir)[0]
                    )
                )
                > 0
            ):

                ids_for_nan_ids = np.intersect1d(
                    np.where(nan_ids[1] == m)[0], np.where(nan_ids[0] == cir)[0]
                )
                w_vel[nan_ids[0][ids_for_nan_ids], nan_ids[1][ids_for_nan_ids]] = np.nan
                print(ids_for_nan_ids, cir, m)
            else:
                w_vel[cir, m] = w_vel[cir, last] - circle.D.isel(circle=cir).isel(
                    alt=m
                ).values * 10 * (m - last)
                last = m

        for n in range(1, len(circle.alt)):

            p_vel[cir, n] = (
                -circle.mean_density.isel(circle=cir).isel(alt=n)
                * 9.81
                * w_vel[cir, n]
                * 60
                * 60
                / 100
            )

    circle["W"] = (["circle", "alt"], w_vel)
    circle["omega"] = (["circle", "alt"], p_vel)

    return print("Finished estimating density, W and omega ...")


def get_advection(circles, list_of_parameters=["u", "v", "q", "ta", "p"]):

    for id_, circle in enumerate(circles):
        adv_dicts = {}
        for var in list_of_parameters:
            adv_dicts[f"h_adv_{var}"] = -(circle.u * eval(f"circle.d{var}dx")) - (
                circle.v * eval(f"circle.d{var}dy")
            )
            circle[f"h_adv_{var}"] = (["alt"], adv_dicts[f"h_adv_{var}"])

    return print("Finished estimating advection terms ...")


def get_circle_products(circles):

    # for id_,circle in enumerate(circles) :

    # circles = regress_for_all_circles(circles, list_of_parameters)

    get_div_and_vor(circles)

    get_density_vertical_velocity_and_omega(circles)

    # get_advection(circles)

    print(f"All circle products retrieved!")

    return circles

