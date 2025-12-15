from src.data.preprocess import DS_MAIN
from src.utils.animation_utils import create_animations

# u10 (10m U wind)
create_animations(DS_MAIN, "u10", "coolwarm", "10m U Wind", "m/s")

# v10 (10m V wind)
create_animations(DS_MAIN, "v10", "coolwarm", "10m V Wind", "m/s")

# t2m (2m Temperature)
create_animations(DS_MAIN, "t2m", "coolwarm", "2m Temperature", "C")

# sst (Sea Surface Temperature)
create_animations(DS_MAIN, "sst", "coolwarm", "Sea Surface Temperature", "C")

# sp (Surface Pressure)
create_animations(DS_MAIN, "sp", "viridis", "Surface Pressure", "mm Hg")

# skt (Skin Temperature)
create_animations(DS_MAIN, "skt", "coolwarm", "Skin Temperature", "C")

# tp (Total Precipitation)
create_animations(DS_MAIN, "tp", "Blues", "Total Precipitation", "mm")
