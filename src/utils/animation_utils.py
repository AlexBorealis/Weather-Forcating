from typing import Optional, Text

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable


def create_animations(
    ds: xr.Dataset,
    param: str,
    cmap: str,
    title: str,
    units: str,
    interval: int = 300,
    fps: int = 5,
) -> None:
    fig = plt.figure(figsize=(14, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

    data_all = {
        "u10": ds[param],
        "v10": ds[param],
        "t2m": ds[param] - 273.15,
        "sst": ds[param] - 273.15,
        "sp": ds[param] * 0.00750062,
        "skt": ds[param] - 273.15,
        "tp": ds[param] * 1000,
    }[param]

    global_vmin = float(data_all.min().values)
    global_vmax = float(data_all.max().values)

    if param == "tp":
        global_vmin = max(1e-4, global_vmin)

    cb: Optional[plt.Colorbar] = None
    min_text: Optional[Text] = None
    max_text: Optional[Text] = None

    def update(frame: int):
        nonlocal cb, min_text, max_text

        ax.clear()
        ax.coastlines(linewidth=0.8)  # type: ignore
        ax.gridlines(  # type: ignore
            draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--"
        )

        da = ds[param].isel(valid_time=frame)
        data = {
            "u10": da,
            "v10": da,
            "t2m": da - 273.15,
            "sst": da - 273.15,
            "sp": da * 0.00750062,
            "skt": da - 273.15,
            "tp": da * 1000,
        }[param]

        frame_vmin = float(data.min().values)
        frame_vmax = float(data.max().values)

        norm = LogNorm(vmin=global_vmin, vmax=global_vmax) if param == "tp" else None

        im = data.plot.pcolormesh(
            ax=ax,
            transform=ccrs.PlateCarree(),
            cmap=cmap,
            vmin=global_vmin,
            vmax=global_vmax,
            norm=norm,
            add_colorbar=False,
        )

        if frame == 0:
            cb = fig.colorbar(im, cax=cax, label=units)
            if param == "tp":
                cb.locator = LogLocator(base=10.0, subs=np.arange(0.1, 1.0, 0.1))
                cb.update_ticks()

        if min_text:
            min_text.remove()  # type: ignore
        if max_text:
            max_text.remove()  # type: ignore

        min_text = cb.ax.text(
            1.5,
            0.0,
            f"min: {frame_vmin:.1f}",
            va="bottom",
            ha="left",
            transform=cb.ax.transAxes,
        )
        max_text = cb.ax.text(
            1.5,
            1.0,
            f"max: {frame_vmax:.1f}",
            va="top",
            ha="left",
            transform=cb.ax.transAxes,
        )

        time_str = str(ds.valid_time[frame].values)[:13]
        ax.set_title(f"{title} ({units}) — {time_str} UTC")

        return [im]

    n_frames = ds.sizes["valid_time"]
    anim = FuncAnimation(
        fig,
        update,
        frames=n_frames,
        interval=interval,
        blit=False,
    )

    output_path = f"{param}_animation.gif"
    anim.save(output_path, writer="pillow", fps=fps)
    print(f"Анимация сохранена: {output_path}")

    plt.close(fig)
