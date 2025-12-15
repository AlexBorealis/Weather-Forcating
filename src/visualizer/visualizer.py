import os
import time
from typing import Dict, Optional, Text

import cartopy.crs as ccrs
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from xarray import DataArray, Dataset


class Visualizer:
    def __init__(
        self,
        ds: Dataset,
        interval: int = 300,
        fps: int = 5,
        save_frames: bool = True,
        verbose: bool = True,
    ):
        self.ds = ds
        self.interval = interval
        self.fps = fps
        self.save_frames = save_frames
        self.verbose = verbose

        self.params: Dict[str, DataArray] = {
            "u10": ds["u10"],
            "v10": ds["v10"],
            "t2m": ds["t2m"] - 273.15,
            "sst": ds["sst"] - 273.15,
            "sp": ds["sp"] * 0.00750062,
            "skt": ds["skt"] - 273.15,
            "tp": ds["tp"] * 1000,
        }

    def create_animation(
        self,
        param: str,
        cmap: str,
        title: str,
        units: str,
    ) -> None:
        t0, t1, t2, t3 = 0, 0, 0, 0
        if self.verbose:
            t0 = time.time()

        fig = plt.figure(figsize=(14, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

        global_vmin = float(self.params[param].min().values)
        global_vmax = float(self.params[param].max().values)

        if param == "tp":
            global_vmin = max(1e-4, global_vmin)

        cb: Optional[plt.Colorbar] = None
        min_text: Optional[Text] = None
        max_text: Optional[Text] = None

        if self.verbose:
            t1 = time.time()
            print(f"Variables creation: {(t1 - t0):.2f} s")

        if self.save_frames:
            os.makedirs(f"frames/{param}", exist_ok=True)

        def update(frame: int):
            nonlocal cb, min_text, max_text

            ax.clear()
            ax.coastlines(linewidth=0.8)  # type: ignore
            ax.gridlines(  # type: ignore
                draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--"
            )

            frame_vmin = float(self.params[param].isel(valid_time=frame).min().values)
            frame_vmax = float(self.params[param].isel(valid_time=frame).max().values)

            norm = (
                LogNorm(vmin=global_vmin, vmax=global_vmax) if param == "tp" else None
            )

            im = (
                self.params[param]
                .isel(valid_time=frame)
                .plot.pcolormesh(
                    ax=ax,
                    transform=ccrs.PlateCarree(),
                    cmap=cmap,
                    vmin=global_vmin,
                    vmax=global_vmax,
                    norm=norm,
                    add_colorbar=False,
                )
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

            time_str = str(self.ds.valid_time[frame].values)[:13]
            ax.set_title(f"{title} ({units}) — {time_str} UTC")

            if self.save_frames:
                fig.savefig(f"frames/{param}/frame_{frame:03d}_{time_str}_UTC.png")

            return [im]

        n_frames = self.ds.sizes["valid_time"]
        anim = FuncAnimation(
            fig,
            update,
            frames=n_frames,
            interval=self.interval,
            blit=False,
        )

        if self.verbose:
            t2 = time.time()
            print(f"FuncAnimation init: {(t2 - t1):.2f} ms")

        output_path = f"{param}_animation.gif"
        anim.save(output_path, writer="pillow", fps=self.fps)
        print(f"Анимация сохранена: {output_path}")

        if self.verbose:
            t3 = time.time()
            print(f"Animation save: {(t3 - t1):.2f} s")
            print(f"Total: {(t3 - t0):.2f} s")

        plt.close(fig)
