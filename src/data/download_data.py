import cdsapi
import os

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": ["10m_u_component_of_wind", "2m_temperature", "total_precipitation"],
    "year": ["2024", "2025"],
    "month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
    "day": [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
    ],
    "time": [
        "00:00",
        "12:00",
    ],
    "data_format": "netcdf",
    "download_format": "zip",
    "area": [40, -10, 20, 10],
}

target = os.path.expanduser(
    "~/Documents/study/Netology/dll/diploma_project_dll/Weather-Forcating/data/raw/reanalysis-era5-single-levels.zip"
)
client = cdsapi.Client()
client.retrieve(dataset, request, target)
