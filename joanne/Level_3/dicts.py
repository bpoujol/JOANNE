import datetime
import subprocess
import joanne

list_of_vars = [
    "sounding",
    "launch_time",
    "height",
    "lat",
    "lon",
    "p",
    "T",
    "rh",
    "wspd",
    "wdir",
    "u",
    "v",
    "theta",
    "q",
    "PW",
    # "static_stability",
    "low_height_flag",
    "cloud_flag",
    "Platform",
    "flight_height",
    "flight_lat",
    "flight_lon",
]

nc_attrs = {
    "sounding": {
        "standard_name": "sounding",
        "long_name": "Sonde number",
        "units": "",
        "axis": "T",
    },
    "launch_time": {
        "standard_name": "time",
        "long_name": "Time of dropsonde launch",
        "units": "seconds since 1970-01-01 00:00:00 UTC",
        "calendar": "gregorian",
        "axis": "T",
    },
    "height": {
        "standard_name": "geopotential_height",
        "long_name": "Geopotential Height",
        "description": "Height obtained by integrating upwards the atmospheric thickness estimated from the hypsometric equation",
        "units": "m",
        "axis": "Z",
        "positive": "up",
    },
    "lat": {
        "standard_name": "latitude",
        "long_name": "North Latitude",
        "units": "degrees_north",
        "axis": "X",
    },
    "lon": {
        "standard_name": "longitude",
        "long_name": "East Longitude",
        "units": "degrees_east",
        "axis": "Y",
    },
    "p": {
        "standard_name": "air_pressure",
        "long_name": "Atmospheric Pressure",
        "units": "hPa",
        "coordinates": "launch_time longitude latitude height",
    },
    "T": {
        "standard_name": "air_temperature",
        "long_name": "Dry Bulb Temperature",
        "units": "degree_Celsius",
        "coordinates": "launch_time longitude latitude height",
    },
    "theta": {
        "standard_name": "potential_temperature",
        "long_name": "potential temperature",
        "units": "K",
        "coordinates": "launch_time longitude latitude height",
    },
    "rh": {
        "standard_name": "relative_humidity",
        "long_name": "Relative Humidity",
        "units": "%",
        "coordinates": "launch_time longitude latitude height",
    },
    "q": {
        "standard_name": "specific_humidity",
        "long_name": "Specific humidity",
        "units": "kg kg-1",
        "coordinates": "launch_time longitude latitude height",
    },
    "wspd": {
        "standard_name": "wind_speed",
        "long_name": "Wind Speed",
        "units": "m s-1",
        "coordinates": "launch_time longitude latitude height",
    },
    "u": {
        "standard_name": "eastward_wind",
        "long_name": "u-component of the wind",
        "units": "m s-1",
        "coordinates": "launch_time longitude latitude height",
    },
    "v": {
        "standard_name": "northward_wind",
        "long_name": "v-component of the wind",
        "units": "m s-1",
        "coordinates": "launch_time longitude latitude height",
    },
    "wdir": {
        "standard_name": "wind_from_direction",
        "long_name": "Wind Direction",
        "units": "degrees",
        "coordinates": "launch_time longitude latitude height",
    },
    "PW": {
        "standard_name": "precipitable_water",
        "long_name": "integrated water vapour in the measured column",
        "units": "kg m-2",
        "coordinates": "launch_time",
    },
    "static_stability": {
        "standard_name": "static_stability",
        "long_name": "static stability",
        "description": "gradient of potential temperature along the pressure grid",
        "units": "K hPa-1",
        "coordinates": "launch_time longitude latitude height",
    },
    "low_height_flag": {
        "long_name": "flag to indicate if flight height at launch was low",
        "flag_values": "1, 0",
        "flag_meanings": "flight height below 4 km flight height at or above 4 km",
        "units": "",
        "valid_range": "0, 1",
    },
    "cloud_flag": {
        "long_name": "flag to indicate presence of cloud",
        "flag_values": "1, 0",
        "flag_meanings": "cloud no_cloud",
        "units": "",
        "valid_range": "0, 1",
    },
    "Platform": {
        "standard_name": "platform",
        "long_name": "platform from which the sounding was made",
        "units": "",
        "coordinates": "launch_time",
    },
    "flight_height": {
        "standard_name": "height",
        "long_name": "height of the aircraft when the dropsonde was launched",
        "units": "m",
        "coordinates": "launch_time",
    },
    "flight_lat": {
        "standard_name": "latitude",
        "long_name": "north latitude of the aircraft when the dropsonde was launched",
        "units": "degrees_north",
        "coordinates": "launch_time",
    },
    "flight_lon": {
        "standard_name": "longitude",
        "long_name": "east longitude of the aircraft when the dropsonde was launched",
        "units": "degrees_east",
        "coordinates": "launch_time",
    },
}

nc_dims = {
    "sounding": ["sounding"],
    "launch_time": ["sounding"],
    "height": ["height"],
    "lat": ["sounding", "height"],
    "lon": ["sounding", "height"],
    "p": ["sounding", "height"],
    "T": ["sounding", "height"],
    "rh": ["sounding", "height"],
    "wspd": ["sounding", "height"],
    "wdir": ["sounding", "height"],
    "u": ["sounding", "height"],
    "v": ["sounding", "height"],
    "theta": ["sounding", "height"],
    "q": ["sounding", "height"],
    "PW": ["sounding"],
    "static_stability": ["sounding", "height"],
    "low_height_flag": ["sounding"],
    "cloud_flag": ["sounding", "height"],
    "Platform": ["sounding"],
    "flight_height": ["sounding"],
    "flight_lat": ["sounding"],
    "flight_lon": ["sounding"],
}

nc_global_attrs = {
    "title": "EUREC4A JOANNE Level-3",
    "Conventions": "CF-1.8",
    "campaign_id": "EUREC4A",
    "project_id" : "JOANNE",
    "instrument_id": "Vaisala RD-41",
    "product_id" : 'Level-3',
    "AVAPS-Software-version" = "Version 4.1.2",
    "ASPEN-version": "BatchAspen v3.4.3",
    "JOANNE-version": joanne.__version__,
    "author": "Geet George",
    "author_email": "geet.george@mpimet.mpg.de",
    "featureType": "trajectory",
    "creation_time": str(datetime.datetime.utcnow()) + " UTC",
}
