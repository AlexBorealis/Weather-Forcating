import os
import time
from typing import Dict, Optional, Text, Tuple, Union

import cartopy.crs as ccrs
import matplotlib.ticker as mticker
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from xarray import DataArray, Dataset

from src.visualizer.kde import kde1d, kde2d


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

    def _global_extremum(self, param: str) -> Tuple:
        """Подготовка глобальных min/max для параметра."""
        global_vmin = float(self.params[param].min().values)
        global_vmax = float(self.params[param].max().values)
        if param == "tp":
            global_vmin = max(1e-4, global_vmin)
        return global_vmin, global_vmax

    def _update_map_frame(
        self,
        frame: int,
        ax: plt.Axes,
        cax: plt.Axes,
        param: str,
        cmap: str,
        title: str,
        units: str,
        cb: Optional[plt.colorbar],
        min_text: Optional[Text],
        max_text: Optional[Text],
        global_vmin: float,
        global_vmax: float,
    ) -> Tuple:
        """Обновление кадра для типа 'map'."""
        ax.clear()
        ax.set_global()  # type: ignore
        ax.coastlines(linewidth=0.8)  # type: ignore
        gl = ax.gridlines(  # type: ignore
            draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--"
        )
        gl.xlocator = mticker.FixedLocator(np.arange(-180, 181, 15))
        gl.ylocator = mticker.FixedLocator(np.arange(-90, 91, 15))

        ax.set_xticks([])
        ax.set_yticks([])

        frame_vmin = float(self.params[param].isel(valid_time=frame).min().values)
        frame_vmax = float(self.params[param].isel(valid_time=frame).max().values)

        norm = LogNorm(vmin=global_vmin, vmax=global_vmax) if param == "tp" else None

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

        ax.set_xlabel("Longitude")
        ax.xaxis.labelpad = 20

        ax.set_ylabel("Latitude")
        ax.yaxis.labelpad = 20

        if cb is None:
            cb = plt.colorbar(im, cax=cax, label=units)
            if param == "tp":
                cb.locator = LogLocator(base=10.0, subs=np.arange(0.1, 1.0, 0.1))
                cb.update_ticks()

        if min_text:
            min_text.remove()  # type: ignore
        if max_text:
            max_text.remove()  # type: ignore

        min_text = cax.text(
            1.5,
            0.0,
            f"min: {frame_vmin:.1f}",
            va="bottom",
            ha="left",
            transform=cax.transAxes,
        )
        max_text = cax.text(
            1.5,
            1.0,
            f"max: {frame_vmax:.1f}",
            va="top",
            ha="left",
            transform=cax.transAxes,
        )

        time_str = str(self.ds.valid_time[frame].values)[:13]
        ax.set_title(f"{title} ({units}) — {time_str} UTC")

        if self.save_frames:
            os.makedirs(f"frames/map/{param}", exist_ok=True)
            plt.savefig(f"frames/map/{param}/frame_{frame:03d}_{time_str}_UTC.png")

        return [im], cb, min_text, max_text

    def _update_kde1d_frame(
        self,
        frame: int,
        ax: plt.Axes,
        param: str,
        title: str,
        units: str,
        bins: int = 100,
        smooth_sigma: float = 1.0,
    ) -> list:
        """Обновление кадра для типа 'kde1d'."""
        ax.clear()

        kde_data = kde1d(
            self.ds, param, frame=frame, bins=bins, smooth_sigma=smooth_sigma
        )
        bin_centers = kde_data["bin_centers"]
        hist = kde_data["hist"]
        density = kde_data["density"]

        ax.bar(
            bin_centers,
            hist,
            width=(bin_centers[1] - bin_centers[0]),
            alpha=0.5,
            color="gray",
            label="Histogram",
        )
        ax.plot(bin_centers, density, color="blue", label="KDE")
        ax.axvline(kde_data["mean"], color="red", linestyle="--", label="Mean")
        ax.axvline(kde_data["median"], color="green", linestyle=":", label="Median")
        ax.axvline(kde_data["v_min"], color="red", linestyle="-.", label="Min")
        ax.axvline(kde_data["v_max"], color="red", linestyle="-.", label="Max")

        ax.set_xlabel(f"{param.upper()} ({units})")
        ax.set_ylabel("Density")
        time_str = str(self.ds.valid_time[frame].values)[:13]
        ax.set_title(f"KDE 1D: {title} at {time_str} UTC")
        ax.legend()

        if self.save_frames:
            os.makedirs(f"frames/kde1d/{param}", exist_ok=True)
            plt.savefig(f"frames/kde1d/{param}/frame_{frame:03d}_{time_str}_UTC.png")

        return ax.get_children()

    def create_animation(
        self,
        vis_type: str = "map",
        param: str = None,
        cmap: str = "viridis",
        title: str = None,
        units: str = "",
        bins: Union[int, Tuple[int, int]] = 100,
        smooth_sigma: float = 1.0,
    ) -> None:
        """Обобщенный метод для создания анимаций разных типов визуализаций."""
        if vis_type not in ["map", "kde1d"]:
            raise ValueError("vis_type must be one of: 'map', 'kde1d'")

        if vis_type in ["map", "kde1d"] and param is None:
            raise ValueError("param is required for 'map' and 'kde1d'")

        os.makedirs("animations/map", exist_ok=True)
        os.makedirs("animations/kde1d", exist_ok=True)

        t0 = time.time() if self.verbose else None

        fig = (
            plt.figure(figsize=(20, 12))
            if vis_type == "map"
            else plt.figure(figsize=(14, 8))
        )
        ax = plt.axes(projection=ccrs.PlateCarree()) if vis_type == "map" else plt.gca()
        divider = make_axes_locatable(ax) if vis_type == "map" else None
        cax = (
            divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)
            if vis_type == "map"
            else None
        )

        global_vmin, global_vmax = (
            self._global_extremum(param) if vis_type == "map" else (None, None)
        )
        cb = None
        min_text = None
        max_text = None

        n_frames = self.ds.sizes["valid_time"]

        def update(frame: int):
            nonlocal cb, min_text, max_text

            if vis_type == "map":
                ret, cb, min_text, max_text = self._update_map_frame(
                    frame,
                    ax,
                    cax,
                    param,
                    cmap,
                    title,
                    units,
                    cb,
                    min_text,
                    max_text,
                    global_vmin,
                    global_vmax,
                )
                return ret
            else:
                return self._update_kde1d_frame(
                    frame, ax, param, title, units, bins, smooth_sigma
                )

        anim = FuncAnimation(
            fig,
            update,
            frames=n_frames,
            interval=self.interval,
            blit=False,
        )

        if self.verbose:
            t2 = time.time()
            print(f"FuncAnimation init: {(t2 - t0):.2f} s")

        # Определение имени файла на основе типа
        if vis_type == "map":
            output_path = f"animations/map/{param}_animation.gif"
        else:
            output_path = f"animations/kde1d/{param}_animation.gif"

        anim.save(output_path, writer="pillow", fps=self.fps)

        if self.verbose:
            t3 = time.time()
            print(f"Animation save: {(t3 - t0):.2f} s")
            print(f"Total: {(t3 - t0):.2f} s")

        plt.close(fig)

    def plot_kde2d(
        self,
        param_y: str,
        param_x: str,
        cmap: str = "magma",
        title: str = None,
        units_y: str = "",
        units_x: str = "",
        frame: Union[int, slice, None] = None,
        bins: Union[int, Tuple[int, int]] = 100,
        smooth_sigma: float = 1.0,
        contour: bool = True,
        save_path: str = None,
    ) -> None:
        """
        Создаёт статическую 2D KDE визуализацию (тепловая карта плотности).
        """
        kde_data = kde2d(
            self.ds,
            param_x=param_x,
            param_y=param_y,
            bins_y=bins,
            smooth_sigma=smooth_sigma,
            frame=frame,
        )

        # Вычисляем центры бинов для contour (важно!)
        x_centers = (kde_data["x_edges"][:-1] + kde_data["x_edges"][1:]) / 2
        y_centers = (kde_data["y_edges"][:-1] + kde_data["y_edges"][1:]) / 2

        # Сетка центров для contour
        X_centers, Y_centers = np.meshgrid(x_centers, y_centers)

        fig, ax = plt.subplots(figsize=(12, 8))

        # Тепловая карта — используем края (как и раньше)
        im = ax.pcolormesh(
            kde_data["X"] if param_x != "latitude" else kde_data["Y"],
            kde_data["Y"] if param_x != "latitude" else kde_data["X"],
            kde_data["ndensity"].T,
            cmap=cmap,
            shading="auto",
        )

        # Контуры — только по центрам!
        if contour:
            cs = ax.contour(
                X_centers if param_x != "latitude" else Y_centers,
                Y_centers if param_x != "latitude" else X_centers,
                kde_data["ndensity"].T,
                levels=8,
                colors="white",
                alpha=0.5,
                linewidths=1.0,
            )
            ax.clabel(cs, inline=True, fontsize=11, colors="black", fmt="%d")

        # Цветовая шкала
        plt.colorbar(im, ax=ax, label="Плотность вероятности (%)", shrink=0.8)

        # Подписи осей
        if param_x != "latitude":
            ax.set_xlabel(f"{param_x.capitalize()} ({units_x})")
            ax.set_ylabel(f"{param_y.upper()} ({units_y})")
            ax.scatter(
                kde_data["x_unique"],
                kde_data["min_per_x"],
                color="red",
                s=6,
                label="Min",
            )
            ax.scatter(
                kde_data["x_unique"],
                kde_data["max_per_x"],
                color="red",
                s=6,
                label="Max",
            )
        else:
            ax.set_ylabel(f"{param_x.capitalize()} ({units_x})")
            ax.set_xlabel(f"{param_y.upper()} ({units_y})")
            ax.scatter(
                kde_data["min_per_x"],
                kde_data["x_unique"],
                color="red",
                s=6,
                label="Min",
            )
            ax.scatter(
                kde_data["max_per_x"],
                kde_data["x_unique"],
                color="red",
                s=6,
                label="Max",
            )

        # Заголовок
        time_info = ""
        if frame is not None:
            try:
                time_str = str(self.ds.valid_time.isel(valid_time=frame).values)[:13]
                time_info = f" — {time_str} UTC"
            except:
                pass

        title = title or f"KDE 2D: {param_y.upper()} vs {param_x.upper()}"
        ax.set_title(f"{title}{time_info}", fontsize=14, pad=15)

        ax.grid(True, alpha=0.3)

        # Сохранение
        if save_path is None:
            os.makedirs("frames/kde2d", exist_ok=True)
            suffix = f"_{param_y}_vs_{param_x}"
            if frame is not None:
                suffix += f"_frame_{frame}"
            save_path = f"frames/kde2d/kde2d{suffix}.png"

        fig.savefig(save_path, dpi=200, bbox_inches="tight")

        plt.close(fig)
