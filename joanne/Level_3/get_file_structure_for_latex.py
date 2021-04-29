# %%
from joanne.Level_3 import dicts
import joanne

from importlib import reload

reload(dicts)

# %%
dicts.list_of_vars

directory = "/Users/geet/Documents/JOANNE/joanne/Level_3/"

var_name = dicts.list_of_vars

Dimensions = []
Coordinates = ["alt", "lat", "lon", "sonde_id"]
Variables = [
    var for var in var_name if (var not in Dimensions) & (var not in Coordinates)
]


def string_table_row(var):

    desc = dicts.nc_attrs[var]["long_name"]
    if var not in ["launch_time", "interpolated_time"]:
        units = dicts.nc_attrs[var]["units"]
    else:
        units = "seconds since 2020-01-01"
    dims_list = dicts.nc_dims[var]
    dims = ", ".join(dims_list)
    str_trow = f" & {var} & {desc} & {units} & {dims} \\\ \\hline \n"

    return str_trow


def rows_for_objects(Object):

    id_ = 0
    for i in var_name:
        if i in eval(Object):
            if id_ == 0:
                file.write(f"{Object}" + string_table_row(i))
                id_ += 1
            else:
                file.write(string_table_row(i))
                id_ += 1


file = open(f"{directory}latex_table_Level_3_v{joanne.__version__}.txt", "w",)

file.write("\\begin{table}[H]\n")
file.write("\\centering\n")
file.write(
    "\caption{Table shows the structure for the Level-3 product, outlining the coordinates, variables and their corresponding descriptions, units and dimensions.}\n"
)
file.write("\label{l3}\n")
file.write(
    "\\begin{tabular}{p{0.08\\linewidth} p{0.12\\linewidth} p{0.3\\linewidth} p{0.2\\linewidth} p{0.12\\linewidth}}\n"
)
file.write("\\hline\n")
file.write("OBJECT & NAME & DESCRIPTION & UNITS & DIMENSION \\\ \\hline \\hline\n")

for Object in ["Dimensions", "Coordinates", "Variables"]:
    rows_for_objects(Object)

file.write("\\end{tabular}\n")


file.write("\\end{table}")

file.close()
# %%

