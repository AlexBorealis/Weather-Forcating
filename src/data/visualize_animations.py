from src.data.preprocess import DS_MAIN
from src.visualizer.visualizer import Visualizer

visualizer = Visualizer(DS_MAIN)

# u10 (10m U wind)
visualizer.create_animation("u10", "coolwarm", "10m U Wind", "m/s")

# v10 (10m V wind)
visualizer.create_animation("v10", "coolwarm", "10m V Wind", "m/s")

# t2m (2m Temperature)
visualizer.create_animation("t2m", "coolwarm", "2m Temperature", "C")

# sst (Sea Surface Temperature)
visualizer.create_animation("sst", "coolwarm", "Sea Surface Temperature", "C")

# sp (Surface Pressure)
visualizer.create_animation("sp", "viridis", "Surface Pressure", "mm Hg")

# skt (Skin Temperature)
visualizer.create_animation("skt", "coolwarm", "Skin Temperature", "C")

# tp (Total Precipitation)
visualizer.create_animation("tp", "Blues", "Total Precipitation", "mm")
