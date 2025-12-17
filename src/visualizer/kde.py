from typing import Dict, Tuple, Union

import numpy as np
from scipy.ndimage import gaussian_filter, gaussian_filter1d
from xarray import Dataset

from src.utils.params import get_param


def kde1d(
    ds: Dataset,
    param: str,
    frame: Union[int, slice, None] = None,
    bins: int = 100,
    smooth_sigma: float = 1.0,
) -> Dict:
    values_clean = get_param(ds, param, frame)["values_clean"]

    if param in ["t2m", "sst", "skt"]:
        values_clean = values_clean - 273.15
    elif param == "sp":
        values_clean = values_clean * 0.00750062
    elif param == "tp":
        values_clean = values_clean * 1000

    if len(values_clean) == 0:
        raise ValueError("No valid data")

    v_min, v_max = values_clean.min(), values_clean.max()
    if v_min == v_max:
        raise ValueError("All values are identical")

    hist, bin_edges = np.histogram(
        values_clean, bins=bins, range=(v_min, v_max), density=True
    )
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    if smooth_sigma > 0:
        density = gaussian_filter1d(hist, sigma=smooth_sigma)
    else:
        density = hist.copy()

    density_max = density.max()
    if density_max > 0:
        ndensity = (density / density_max) * 100.0
    else:
        ndensity = density.copy()

    result = {
        "bin_centers": bin_centers,
        "hist": hist,
        "density": density,
        "ndensity": ndensity,
        "v_min": v_min,
        "mean": values_clean.mean(),
        "median": np.median(values_clean),
        "v_max": v_max,
    }

    return result


def kde2d(
    ds: Dataset,
    param_x: str,
    param_y: str,
    bins_y: Union[int, Tuple[int, int]] = 100,
    smooth_sigma: float = 1.0,
    frame: Union[int, slice, None] = None,
) -> Dict:
    # Получаем данные для Y (основной параметр)
    y_data = get_param(ds, param_y, frame)
    p_y_clean = y_data["values_clean"]
    valid_indices = y_data["indices"]  # индексы валидных значений в полном массиве

    # Преобразование единиц для Y
    if param_y in ["t2m", "sst", "skt"]:
        p_y = p_y_clean - 273.15
    elif param_y == "sp":
        p_y = p_y_clean * 0.00750062
    elif param_y == "tp":
        p_y = p_y_clean * 1000
    else:
        p_y = p_y_clean

    # Получаем координаты (без фильтрации NaN — они полные)
    time_data = get_param(ds, "valid_time", frame)
    lat_data = get_param(ds, "latitude", frame)
    lon_data = get_param(ds, "longitude", frame)

    n_time = time_data["values"].size
    n_lat = lat_data["values"].size
    n_lon = lon_data["values"].size

    # Создаём полный массив p_x (до фильтрации)
    if param_x == "valid_time":
        hours = time_data["values"].astype("datetime64[h]").astype(int) % 24
        p_x_full = np.repeat(hours, n_lat * n_lon)
        bins_x = len(np.unique(hours))
    elif param_x == "latitude":
        p_x_full = np.tile(np.repeat(lat_data["values"], n_lon), n_time)
        bins_x = n_lat // 10
    elif param_x == "longitude":
        p_x_full = np.tile(lon_data["values"], n_time * n_lat)
        bins_x = n_lon // 10
    else:
        raise ValueError("param_x must be 'valid_time', 'latitude' or 'longitude'")

    # Применяем ту же маску валидности, что и для p_y
    p_x = p_x_full[valid_indices]

    if len(p_x) == 0 or len(p_y) == 0:
        raise ValueError("No valid data after filtering NaN")

    unique_x = np.unique(p_x)
    min_per_x = np.array([p_y[p_x == val].min() for val in unique_x])
    max_per_x = np.array([p_y[p_x == val].max() for val in unique_x])

    x_range = (p_x.min(), p_x.max())
    y_range = (p_y.min(), p_y.max())

    hist, x_edges, y_edges = np.histogram2d(
        p_x,
        p_y,
        bins=[bins_x, bins_y],
        range=[x_range, y_range],
        density=True,
    )

    density = (
        gaussian_filter(hist, sigma=smooth_sigma) if smooth_sigma > 0 else hist.copy()
    )

    density_max = density.max()
    ndensity = (density / density_max * 100.0) if density_max > 0 else density.copy()

    X, Y = np.meshgrid(x_edges, y_edges)

    return {
        "X": X,
        "Y": Y,
        "density": density,
        "ndensity": ndensity,
        "x_edges": x_edges,
        "y_edges": y_edges,
        "x_range": x_range,
        "y_range": y_range,
        "density_max": float(density_max),
        "x_unique": unique_x,
        "min_per_x": min_per_x,
        "max_per_x": max_per_x,
    }
