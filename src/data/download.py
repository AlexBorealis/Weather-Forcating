import os

import cdsapi
from dotenv import load_dotenv

from src.utils.parse_args import parse_args

load_dotenv()

# Set project directory
os.chdir(os.getenv("PROJECT_DIR"))

DATASET_NAME = (
    "era5-"
    + f"{parse_args.start_month}-{parse_args.start_day}-{parse_args.start_year}--"
    + f"{parse_args.end_month}-{parse_args.end_day}-{parse_args.end_year}"
    + ".zip"
)


# Create body request
dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_temperature",
        "sea_surface_temperature",
        "surface_pressure",
        "total_precipitation",
        "skin_temperature",
    ],
    "year": [
        str(year)
        for year in range(int(parse_args.start_year), int(parse_args.end_year) + 1)
    ],
    "month": [
        "{:02}".format(month)
        for month in range(int(parse_args.start_month), int(parse_args.end_month) + 1)
    ],
    "day": [
        "{:02}".format(day)
        for day in range(int(parse_args.start_day), int(parse_args.end_day) + 1)
    ],
    "time": ["{:02}:00".format(hour) for hour in range(24)],
    "data_format": "netcdf",
    "download_format": "zip",
}


if all(
    v is not None
    for v in [parse_args.north, parse_args.south, parse_args.east, parse_args.west]
):
    request["area"] = [
        parse_args.north,
        parse_args.west,
        parse_args.south,
        parse_args.east,
    ]  # порядок: North, West, South, East

# Create request
target = os.path.join(os.getenv("PROJECT_DIR"), "data", "raw", DATASET_NAME)
client = cdsapi.Client(progress=True)
client.retrieve(dataset, request, target)
