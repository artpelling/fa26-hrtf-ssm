from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from irdl import FabianDataset
from pymor.core.cache import disable_caching

from src.plotting import (
    COLUMN_WIDTH_IN,
    GOLDEN_RATIO,
    HSV_FIGURE_SIZE,
    SELECTED_ORDER_MARKER_STYLE,
    golden_axes,
)
from src.utils import REDUCED_ORDER, dB, make_era


OUTPUT_DIR = Path("generated/figures")
HSV_MAP = Path("generated/data/hsv-map.npy")
ITD_REMOVED_HSV_MAP = Path("generated/data/hsv-map-itd-removed.npy")
HSV_COLORBAR = OUTPUT_DIR / "hsv-colorbar.pdf"
FLOOR_DB = -75
PLOT_BOTTOM = 0.22
PLOT_WIDTH = 0.77
PLOT_HEIGHT = PLOT_WIDTH / GOLDEN_RATIO * COLUMN_WIDTH_IN / HSV_FIGURE_SIZE[1]


def compute_hsv_map(impulse_response, path, delay_removal=None):
    """Compute and persist the HSV map for one delay-removal strategy."""
    # Each width has a unique SVD; retaining every factorization exhausts memory.
    disable_caching()
    n_values = 600
    era, _, n_virtual = make_era(impulse_response, delay_removal)
    values = np.empty((n_values, n_virtual))
    values[:2] = 0

    path.parent.mkdir(parents=True, exist_ok=True)
    for i in range(2, n_values):
        values[i] = era.reductor._sv_U_V(None, min(i, n_virtual))[0][:n_virtual]
        np.save(path, values)


def compute_map():
    """Compute the original-delay HRIR Hankel singular-value map."""
    compute_hsv_map(FabianDataset.get(hato=0, cache_dir="data")["impulse_response"], HSV_MAP)


def compute_itd_removed_map():
    """Compute the map after individual ITD removal."""
    compute_hsv_map(
        FabianDataset.get(hato=0, cache_dir="data")["impulse_response"],
        ITD_REMOVED_HSV_MAP,
        delay_removal="individual",
    )


def plot_hsv_map(values, *, ylabel=True):
    """Create a 2D HSV contour plot with a fixed-size data area."""
    input_counts = np.arange(2, values.shape[0])
    values = values[2:]
    virtual_inputs, singular_value = np.meshgrid(input_counts, np.arange(1, values.shape[1] + 1))
    levels = np.maximum(dB(values, ref=values.max()), FLOOR_DB).T
    solid_levels = np.arange(-72, 1, 12)
    dashed_levels = np.arange(-66, 0, 12)
    dotted_levels = np.arange(-69, 0, 6)
    figure = plt.figure(figsize=HSV_FIGURE_SIZE)
    axis = figure.add_axes((0.16, PLOT_BOTTOM, PLOT_WIDTH, PLOT_HEIGHT))
    golden_axes(axis)
    image = axis.imshow(
        levels,
        cmap="viridis",
        vmin=FLOOR_DB,
        vmax=0,
        extent=(input_counts[0] - 0.5, input_counts[-1] + 0.5, 0.5, values.shape[1] + 0.5),
        origin="lower",
        interpolation="bilinear",
        aspect="auto",
    )
    for contour_levels, linestyle in (
        (solid_levels, "solid"),
        (dashed_levels, "dashed"),
        (dotted_levels, "dotted"),
    ):
        axis.contour(
            virtual_inputs,
            singular_value,
            levels,
            levels=contour_levels,
            colors="black",
            linewidths=0.5,
            linestyles=linestyle,
        )
    rank_bound = values.shape[1]
    axis.axvline(rank_bound, color="tab:red", linewidth=1, zorder=3)
    axis.plot(
        rank_bound,
        REDUCED_ORDER,
        linestyle="none",
        zorder=4,
        **SELECTED_ORDER_MARKER_STYLE,
    )
    axis.set(xlabel="Number of virtual inputs")
    if ylabel:
        axis.set_ylabel("Singular-value index")
    axis.set_xticks(np.arange(100, input_counts[-1] + 1, 100))
    axis.set_yticks(np.arange(100, values.shape[1] + 1, 100))
    axis.xaxis.set_label_position("bottom")
    axis.xaxis.tick_bottom()
    axis.invert_yaxis()
    return figure


def plot_colorbar():
    """Create a vertical HSV colorbar with contour-level indicators."""
    figure = plt.figure(figsize=(0.7, HSV_FIGURE_SIZE[1]))
    colorbar_axis = figure.add_axes((0.05, PLOT_BOTTOM, 0.25, PLOT_HEIGHT))
    colorbar = figure.colorbar(
        plt.cm.ScalarMappable(norm=plt.Normalize(FLOOR_DB, 0), cmap="viridis"),
        cax=colorbar_axis,
        orientation="vertical",
        ticks=np.arange(-72, 1, 12),
    )
    for contour_levels, linestyle in (
        (np.arange(-72, 1, 12), "solid"),
        (np.arange(-66, 0, 12), "dashed"),
        (np.arange(-69, 0, 6), "dotted"),
    ):
        colorbar.ax.hlines(
            contour_levels,
            0,
            1,
            colors="black",
            linewidth=0.5,
            linestyles=linestyle,
            transform=colorbar.ax.get_yaxis_transform(),
        )
    colorbar.ax.yaxis.set_label_position("right")
    colorbar.ax.yaxis.tick_right()
    return figure


def main():
    parser = ArgumentParser(description="Plot the Hankel singular-value map.")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, filename, ylabel in (
        (HSV_MAP, "hsv-map.pdf", True),
        (ITD_REMOVED_HSV_MAP, "hsv-map-itd-removed.pdf", False),
    ):
        figure = plot_hsv_map(np.load(path), ylabel=ylabel)
        figure.savefig(OUTPUT_DIR / filename)
        if not args.no_show:
            plt.show()
        plt.close(figure)

    figure = plot_colorbar()
    figure.savefig(HSV_COLORBAR)
    if not args.no_show:
        plt.show()
    plt.close(figure)
