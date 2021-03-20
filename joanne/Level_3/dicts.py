import datetime
import subprocess
import joanne
import numpy as np

dim_attrs = {
    "alt": {
        "standard_name": "geopotential_height",
        "long_name": "Geopotential Height",
        "description": "Height obtained by integrating upwards the atmospheric thickness estimated from the hypsometric equation",
        "units": "m",
        "axis": "Z",
        "positive": "up",
        "bounds": "alt_bnds",
    },
    "sonde_id": {
        "description": "unique sonde ID in the format PLATFORM_FLIGHT-ID_sSONDE-NUMBER-FOR-THE-FLIGHT",
        "long_name": "Sonde identifier",
        "cf_role": "trajectory_id",
        "units": "",
    },
}

list_of_vars = [
    # "sounding",
    "launch_time",
    "interpolated_time",
    # "alt",
    "lat",
    "lon",
    "p",
    "ta",
    "rh",
    "wspd",
    "wdir",
    "u",
    "v",
    "theta",
    "q",
    # "PW",
    # "static_stability",
    "low_height_flag",
    # "cloud_flag",
    "platform",
    "flight_height",
    "flight_lat",
    "flight_lon",
    "sonde_id",
    "N_ptu",
    "N_gps",
    "m_ptu",
    "m_gps",
]

nc_attrs = {
    "sounding": {
        "standard_name": "sounding",
        "long_name": "Sonde number",
        "units": "",
        "axis": "T",
    },
    "sonde_id": {
        "description": "unique sonde ID in the format PLATFORM_FLIGHT-ID_sSONDE-NUMBER-FOR-THE-FLIGHT",
        "long_name": "Sonde identifier",
        "cf_role": "trajectory_id",
        "units": "",
    },
    "launch_time": {
        "standard_name": "time",
        "long_name": "Time of dropsonde launch",
        # "units": "seconds since 2020-01-01 00:00:00 UTC",
        # "calendar": "gregorian",
        "axis": "T",
    },
    "alt": {
        "standard_name": "geopotential_height",
        "long_name": "Geopotential Height",
        "description": "Height obtained by integrating upwards the atmospheric thickness estimated from the hypsometric equation",
        "units": "m",
        "axis": "Z",
        "positive": "up",
    },
    "lat": {
        "standard_name": "latitude",
        "long_name": "Latitude",
        "units": "degrees_north",
        "axis": "Y",
    },
    "lon": {
        "standard_name": "longitude",
        "long_name": "Longitude",
        "units": "degrees_east",
        "axis": "X",
    },
    "p": {
        "standard_name": "air_pressure",
        "long_name": "Atmospheric Pressure",
        "units": "Pa",
        "coordinates": "launch_time lon lat alt",
    },
    "ta": {
        "standard_name": "air_temperature",
        "long_name": "Dry Bulb Temperature",
        "units": "K",
        "coordinates": "launch_time lon lat alt",
    },
    "theta": {
        "standard_name": "potential_temperature",
        "long_name": "Potential Temperature",
        "units": "K",
        "coordinates": "launch_time lon lat alt",
    },
    "rh": {
        "standard_name": "relative_humidity",
        "long_name": "Relative Humidity",
        "units": "",
        "coordinates": "launch_time lon lat alt",
    },
    "q": {
        "standard_name": "specific_humidity",
        "long_name": "Specific humidity",
        "units": "kg kg-1",
        "coordinates": "launch_time lon lat alt",
    },
    "wspd": {
        "standard_name": "wind_speed",
        "long_name": "Wind Speed",
        "units": "m s-1",
        "coordinates": "launch_time lon lat alt",
    },
    "u": {
        "standard_name": "eastward_wind",
        "long_name": "u-component of the wind",
        "units": "m s-1",
        "coordinates": "launch_time lon lat alt",
    },
    "v": {
        "standard_name": "northward_wind",
        "long_name": "v-component of the wind",
        "units": "m s-1",
        "coordinates": "launch_time lon lat alt",
    },
    "wdir": {
        "standard_name": "wind_from_direction",
        "long_name": "Wind Direction",
        "units": "degrees",
        "coordinates": "launch_time lon lat alt",
    },
    # "PW": {
    #     "standard_name": "precipitable_water",
    #     "long_name": "integrated water vapour in the measured column",
    #     "units": "kg m-2",
    #     "coordinates": "launch_time",
    # },
    # "static_stability": {
    #     "standard_name": "static_stability",
    #     "long_name": "static stability",
    #     "description": "gradient of potential temperature along the pressure grid",
    #     "units": "K hPa-1",
    #     "coordinates": "launch_time lon lat alt",
    # },
    "low_height_flag": {
        "long_name": "flag if flight height < 4 km when dropsonde was launched",
        "flag_values": np.array([0, 1], dtype=int),
        "flag_meanings": "flight_height_at_or_above_4_km flight_height_below_4_km",
        "units": "",
        "valid_range": "0, 1",
    },
    # "cloud_flag": {
    #     "long_name": "flag to indicate presence of cloud",
    #     "flag_values": "1, 0",
    #     "flag_meanings": "cloud no_cloud",
    #     "units": "",
    #     "valid_range": "0, 1",
    # },
    "platform": {
        "standard_name": "platform",
        "long_name": "platform from which dropsonde was launched",
        "units": "",
        "coordinates": "launch_time",
    },
    "flight_height": {
        "standard_name": "height",
        "long_name": "height of the aircraft when dropsonde was launched",
        "units": "m",
        "coordinates": "launch_time",
    },
    "flight_lat": {
        "standard_name": "latitude",
        "long_name": "north latitude of the aircraft when dropsonde was launched",
        "units": "degrees_north",
        "coordinates": "launch_time",
    },
    "flight_lon": {
        "standard_name": "longitude",
        "long_name": "east longitude of the aircraft when dropsonde was launched",
        "units": "degrees_east",
        "coordinates": "launch_time",
    },
    "N_ptu": {
        "long_name": "number of observations used to derive level 3 PTU-data",
        "units": "",
        "coordinates": "launch_time lon lat alt",
        "standard_name": "number_of_observations",
    },
    "N_gps": {
        "long_name": "number of observations used to derive level 3 GPS-data",
        "units": "",
        "coordinates": "launch_time lon lat alt",
        "standard_name": "number_of_observations",
    },
    "m_ptu": {
        "long_name": "bin_method",
        "description": "method used to derive Level-3 PTU-data",
        "flag_values": np.array([0, 1, 2], dtype=int),
        "flag_meanings": "no_data interpolation averaging",
        "units": "",
    },
    "m_gps": {
        "long_name": "bin_method",
        "description": "method used to derive Level-3 GPS-data",
        "flag_values": np.array([0, 1, 2], dtype=int),
        "flag_meanings": "no_data interpolation averaging",
        "units": "",
    },
    "interpolated_time": {
        "long_name": "interpolated time",
        "description": "value of time (originally independent dimension) linearly interpolated to altitude grid",
        "coordinates": "launch_time lon lat alt",
        # "units": "seconds since 2020-01-01 00:00:00 UTC",
    },
}

nc_dims = {
    "sounding": ["sonde_id"],
    "sonde_id": ["sonde_id"],
    "launch_time": ["sonde_id"],
    "alt": ["alt"],
    "lat": ["sonde_id", "alt"],
    "lon": ["sonde_id", "alt"],
    "p": ["sonde_id", "alt"],
    "ta": ["sonde_id", "alt"],
    "rh": ["sonde_id", "alt"],
    "wspd": ["sonde_id", "alt"],
    "wdir": ["sonde_id", "alt"],
    "u": ["sonde_id", "alt"],
    "v": ["sonde_id", "alt"],
    "theta": ["sonde_id", "alt"],
    "q": ["sonde_id", "alt"],
    "PW": ["sonde_id"],
    "static_stability": ["sonde_id", "alt"],
    "low_height_flag": ["sonde_id"],
    "cloud_flag": ["sonde_id", "alt"],
    "platform": ["sonde_id"],
    "flight_height": ["sonde_id"],
    "flight_lat": ["sonde_id"],
    "flight_lon": ["sonde_id"],
    "N_ptu": ["sonde_id", "alt"],
    "N_gps": ["sonde_id", "alt"],
    "m_ptu": ["sonde_id", "alt"],
    "m_gps": ["sonde_id", "alt"],
    "interpolated_time": ["sonde_id", "alt"],
}

nc_global_attrs = {
    "title": "EUREC4A JOANNE Level-3",
    "Conventions": "CF-1.8",
    "campaign_id": "EUREC4A",
    "project_id": "JOANNE",
    "instrument_id": "Vaisala RD-41",
    "product_id": "Level-3",
    "AVAPS-Software-version": "Version 4.1.2",
    "ASPEN-version": "BatchAspen v3.4.3",
    "JOANNE-version": joanne.__version__,
    "author": "Geet George",
    "author_email": "geet.george@mpimet.mpg.de",
    "featureType": "trajectory",
    "creation_time": str(datetime.datetime.utcnow()) + " UTC",
}
