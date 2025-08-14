import xarray as xr
import os

ds = xr.open_dataset(
    os.path.join(
        "~/Documents/study/Netology/dll/diploma_project_dll/Weather-Forcating",
        "data/raw/reanalysis-era5-single-levels/data_stream-oper_stepType-instant.nc",
    ),
)

print(ds)

print(ds["t2m"])  # Температура на 2м
print(ds["u10"])  # Ветер (U-компонента)

print(ds["t2m"].mean().compute())
print(ds["t2m"].std().compute())

print(
    ds["t2m"].sel(
        valid_time="2025-08-09", latitude=39.75, longitude=-9.75, method="nearest"
    )
)
