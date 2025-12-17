from typing import Dict, Union

import numpy as np
from xarray import Dataset


def get_param(
    ds: Dataset,
    param: str,
    frame: Union[int, slice, None] = None,
) -> Dict:
    if param in ds.coords:
        data = ds[param]
        if data.ndim > 1:
            # для пространственных координат (lat/lon) — повторяем по времени
            if "time" in data.sizes or "valid_time" in data.sizes:
                data = data.isel(
                    {dim: frame for dim in data.sizes if dim in ["time", "valid_time"]}
                )
            # разворачиваем в 1D так же, как и основную переменную
            values = data.values.flatten()
        else:
            values = data.values
    elif param in ds.data_vars:
        # если это другая переменная
        arr = ds[param]
        if frame is not None:
            arr = arr.isel(valid_time=frame) if "valid_time" in arr.sizes else arr
        values = arr.values.flatten()
    else:
        raise KeyError(f"{param} not found in coords or data_vars")

    not_nan_mask = ~np.isnan(values)
    not_nan_indices = np.flatnonzero(not_nan_mask)
    values_clean = values[not_nan_mask]

    result = {
        "values": values,
        "values_clean": values_clean,
        "indices": not_nan_indices,
    }

    return result
