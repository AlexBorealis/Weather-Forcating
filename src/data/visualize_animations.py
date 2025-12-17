from src.data.preprocess import DS_MAIN
from src.visualizer.visualizer import Visualizer

visualizer = Visualizer(DS_MAIN)

# u10 (10m U wind)
visualizer.create_animation("map", "u10", "coolwarm", "10m U Wind", "m/s")

# v10 (10m V wind)
visualizer.create_animation("map", "v10", "coolwarm", "10m V Wind", "m/s")

# t2m (2m Temperature)
visualizer.create_animation("map", "t2m", "coolwarm", "2m Temperature", "C")

# sst (Sea Surface Temperature)
visualizer.create_animation("map", "sst", "coolwarm", "Sea Surface Temperature", "C")

# sp (Surface Pressure)
visualizer.create_animation("map", "sp", "viridis", "Surface Pressure", "mm Hg")

# skt (Skin Temperature)
visualizer.create_animation("map", "skt", "coolwarm", "Skin Temperature", "C")

# tp (Total Precipitation)
visualizer.create_animation("map", "tp", "Blues", "Total Precipitation", "mm")

# KDE 1D -------------------------------------------------------------------------------
# u10 (10m U wind)
visualizer.create_animation("kde1d", "u10", "coolwarm", "10m U Wind", "m/s")

# v10 (10m V wind)
visualizer.create_animation("kde1d", "v10", "coolwarm", "10m V Wind", "m/s")

# t2m (2m Temperature)
visualizer.create_animation("kde1d", "t2m", "coolwarm", "2m Temperature", "C")

# sst (Sea Surface Temperature)
visualizer.create_animation("kde1d", "sst", "coolwarm", "Sea Surface Temperature", "C")

# sp (Surface Pressure)
visualizer.create_animation("kde1d", "sp", "coolwarm", "Surface Pressure", "mm Hg")

# skt (Skin Temperature)
visualizer.create_animation("kde1d", "skt", "coolwarm", "Skin Temperature", "C")

# tp (Total Precipitation)
visualizer.create_animation("kde1d", "tp", "Blues", "Total Precipitation", "mm")

# KDE 2D -------------------------------------------------------------------------------
# u10 (10m U wind)
visualizer.plot_kde2d("u10", "valid_time", "coolwarm", "10m U Wind", "m/s", "Hours")

visualizer.plot_kde2d("u10", "latitude", "coolwarm", "10m U Wind", "m/s", "Lat")

visualizer.plot_kde2d("u10", "longitude", "coolwarm", "10m U Wind", "m/s", "Long")

# v10 (10m V wind)
visualizer.plot_kde2d("v10", "valid_time", "coolwarm", "10m V Wind", "m/s", "Hours")

visualizer.plot_kde2d("v10", "latitude", "coolwarm", "10m V Wind", "m/s", "Lat")

visualizer.plot_kde2d("v10", "longitude", "coolwarm", "10m V Wind", "m/s", "Long")

# t2m (2m Temperature)
visualizer.plot_kde2d("t2m", "valid_time", "coolwarm", "2m Temperature", "C", "Hours")

visualizer.plot_kde2d("t2m", "latitude", "coolwarm", "2m Temperature", "C", "Lat")

visualizer.plot_kde2d("t2m", "longitude", "coolwarm", "2m Temperature", "C", "Long")

# sst (Sea Surface Temperature)
visualizer.plot_kde2d(
    "sst", "valid_time", "coolwarm", "Sea Surface Temperature", "C", "Hours"
)

visualizer.plot_kde2d(
    "sst", "latitude", "coolwarm", "Sea Surface Temperature", "C", "Lat"
)

visualizer.plot_kde2d(
    "sst", "longitude", "coolwarm", "Sea Surface Temperature", "C", "Long"
)

# sp (Surface Pressure)
visualizer.plot_kde2d(
    "sp", "valid_time", "coolwarm", "Surface Pressure", "m/s", "Hours"
)

visualizer.plot_kde2d("sp", "latitude", "coolwarm", "Surface Pressure", "m/s", "Lat")

visualizer.plot_kde2d("sp", "longitude", "coolwarm", "Surface Pressure", "m/s", "Long")

# skt (Skin Temperature)
visualizer.plot_kde2d("skt", "valid_time", "coolwarm", "Skin Temperature", "C", "Hours")

visualizer.plot_kde2d("skt", "latitude", "coolwarm", "Skin Temperature", "C", "Lat")

visualizer.plot_kde2d("skt", "longitude", "coolwarm", "Skin Temperature", "C", "Long")

# tp (Total Precipitation)
visualizer.plot_kde2d(
    "tp", "valid_time", "coolwarm", "Total Precipitation", "mm", "Hours"
)

visualizer.plot_kde2d("tp", "latitude", "coolwarm", "Total Precipitation", "mm", "Lat")

visualizer.plot_kde2d(
    "tp", "longitude", "coolwarm", "Total Precipitation", "mm", "Long"
)
