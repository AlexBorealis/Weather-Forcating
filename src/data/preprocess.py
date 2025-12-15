import os
import zipfile

import xarray as xr
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.path.join(os.getenv("PROJECT_DIR"), "data", "raw")
EXTRACTED_DIR = os.path.join(os.getenv("PROJECT_DIR"), "data", "processed", "extracted")

archives = os.listdir(DATA_DIR)
archive_names = [arch.replace(".zip", "") for arch in archives]
archives = [os.path.join(DATA_DIR, arch) for arch in archives]
extracted_dirs = [os.path.join(EXTRACTED_DIR, arch) for arch in archive_names]

[os.makedirs(ext, exist_ok=True) for ext in extracted_dirs]

if len(extracted_dirs) == 0 and len(os.listdir(extracted_dirs[-1])) == 0:
    for arch, ext in zip(archives, extracted_dirs):
        with zipfile.ZipFile(arch, "r") as zip_ref:
            zip_ref.extractall(ext)

# last reanalis -----------------------------------------------------------------------
# u10m, v10m, t2m, sst, sp, skt
file_name1 = os.path.join(extracted_dirs[-1], os.listdir(extracted_dirs[-1])[0])
# tp
file_name2 = os.path.join(extracted_dirs[-1], os.listdir(extracted_dirs[-1])[1])

if not os.path.exists(os.path.join(os.path.dirname(file_name1), "all_data.nc")):
    ds1 = xr.open_dataset(file_name1)
    ds2 = xr.open_dataset(file_name2)

    if ds1.sizes == ds2.sizes:
        ds_merged = ds1.merge(ds2, compat="override")
        ds_merged.to_netcdf(os.path.join(os.path.dirname(file_name1), "all_data.nc"))

DS_MAIN = xr.open_dataset(os.path.join(os.path.dirname(file_name1), "all_data.nc"))

# print(DS_MAIN.info())
# print(
#     DS_MAIN["tp"].isel(valid_time=0).min().values,
#     DS_MAIN["tp"].isel(valid_time=0).max().values,
# )
# print(
#     DS_MAIN["sp"].isel(valid_time=0).min().values,
#     DS_MAIN["sp"].isel(valid_time=0).max().values,
# )
# print(
#     DS_MAIN["u10"].isel(valid_time=0).min().values,
#     DS_MAIN["u10"].isel(valid_time=0).max().values,
# )
# print(type(DS_MAIN))
