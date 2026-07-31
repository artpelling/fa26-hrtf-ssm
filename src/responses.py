"""Compute and plot representative measured and ERA-reconstructed FABIAN responses."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pyfar as pf
from irdl import FabianDataset

from src.utils import REDUCED_ORDER, make_era, prepare_impulse_response, restore_delays
from src.plotting import COLUMN_WIDTH_IN, golden_axes, plot_color


RESULTS = Path("generated/data/responses.npz")
OUTPUT_DIR = Path("generated/figures")
MODEL_ORDERS = (REDUCED_ORDER,)
TIME_LIMITS = (-1, 1)
FREQUENCY_LIMITS = (-48, 20)
# Front-right, slightly elevated incident direction, in radians.
DIRECTION = (np.pi / 4, np.pi / 12)
OUTPUTS = (
    OUTPUT_DIR / "responses-itd-removed-time.pdf",
    OUTPUT_DIR / "responses-frequency.pdf",
    OUTPUT_DIR / "responses-legend.pdf",
)
ITD_MODEL_COLORS = (plot_color("left_ear"), plot_color("right_ear"))
ITD_ERROR_COLORS = (plot_color("left_ear", 1), plot_color("right_ear", 1))
RAW_MODEL_COLORS = (plot_color("no_removal"), plot_color("itd_removal"))
RAW_ERROR_COLORS = (plot_color("no_removal", 1), plot_color("itd_removal", 1))


def _direction_index(coordinates):
    """Return the FABIAN direction nearest to the requested incident direction."""
    azimuth, elevation = DIRECTION
    return np.argmin(
        (coordinates.elevation - elevation) ** 2
        + np.angle(np.exp(1j * (coordinates.azimuth - azimuth))) ** 2
    )


def compute():
    """Persist measured HRIRs and original-delay and ITD-removed ERA reconstructions."""
    data = FabianDataset.get(hato=0, cache_dir="data")
    hrir = prepare_impulse_response(data["impulse_response"])

    era, _, n_virtual = make_era(hrir)
    n_response_samples = era.reductor.data.shape[0] + 1
    raw_reconstructed = np.asarray(
        [
            era.reduce(order, num_right=n_virtual).impulse_response(n_response_samples).time
            for order in MODEL_ORDERS
        ]
    )

    itd_era, _, itd_n_virtual = make_era(hrir, delay_removal="individual")
    itd_n_response_samples = itd_era.reductor.data.shape[0] + 1
    itd_reconstructed = np.asarray(
        [
            restore_delays(
                itd_era.reduce(order, num_right=itd_n_virtual).impulse_response(itd_n_response_samples),
                hrir,
                delay_removal="individual",
            ).time
            for order in MODEL_ORDERS
        ]
    )

    index = _direction_index(data["source_coordinates"])
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        RESULTS,
        measured=hrir[index, :].time,
        raw_reconstructed=raw_reconstructed[:, index, :, :],
        itd_reconstructed=itd_reconstructed[:, index, :, :],
    )


def _finish_panel(axis):
    axis.minorticks_on()
    axis.grid(which="major", alpha=0.3)
    axis.grid(which="minor", alpha=0.15, linewidth=0.5)


def plot_time(measured, reconstructed):
    """Plot individually ITD-removed reconstructed and measured responses."""
    figure, axis = plt.subplots(figsize=(COLUMN_WIDTH_IN, 2.8), layout="constrained")
    for ear in range(len(ITD_MODEL_COLORS)):
        actual = pf.Signal(measured[ear], 44_100)
        pf.plot.time(actual, unit="ms", ax=axis, color="black", linewidth=2)
    for ear, model_color in enumerate(ITD_MODEL_COLORS):
        model = pf.Signal(reconstructed[0, ear], 44_100)
        pf.plot.time(model, unit="ms", ax=axis, color=model_color)
    axis.set(xlim=(0, 2.5), ylim=TIME_LIMITS)
    golden_axes(axis)
    _finish_panel(axis)
    return figure


def plot_frequency(measured, raw_reconstructed, itd_reconstructed):
    """Plot both reconstruction methods, their errors, and the measured responses."""
    figure, axis = plt.subplots(figsize=(COLUMN_WIDTH_IN, 2.8), layout="constrained")
    for ear in range(len(ITD_MODEL_COLORS)):
        actual = pf.Signal(measured[ear], 44_100)
        pf.plot.freq(actual, ax=axis, color="black", linewidth=2)
    for reconstructed, model_colors, error_colors, linestyle in (
        (raw_reconstructed, RAW_MODEL_COLORS, RAW_ERROR_COLORS, "--"),
        (itd_reconstructed, ITD_MODEL_COLORS, ITD_ERROR_COLORS, "-"),
    ):
        for ear, (model_color, error_color) in enumerate(zip(model_colors, error_colors)):
            actual = pf.Signal(measured[ear], 44_100)
            model = pf.Signal(reconstructed[0, ear], 44_100)
            pf.plot.freq(actual - model, ax=axis, color=error_color, linestyle=linestyle, linewidth=0.75)
            pf.plot.freq(model, ax=axis, color=model_color, linestyle=linestyle)
    axis.set(ylim=FREQUENCY_LIMITS)
    golden_axes(axis)
    _finish_panel(axis)
    return figure


def plot_legend():
    """Create a compact shared legend explaining data, models, and errors."""
    figure, axis = plt.subplots(figsize=(2 * COLUMN_WIDTH_IN, 0.85), layout="constrained")
    axis.axis("off")
    handles = (
        Line2D([], [], color="black", linewidth=2, label="Measured data"),
        Line2D([], [], color=ITD_MODEL_COLORS[0], label="ITD model, left"),
        Line2D([], [], color=ITD_MODEL_COLORS[1], label="ITD model, right"),
        Line2D([], [], color=RAW_MODEL_COLORS[0], linestyle="--", label="Original-delay model, left"),
        Line2D([], [], color=RAW_MODEL_COLORS[1], linestyle="--", label="Original-delay model, right"),
        Line2D([], [], color=ITD_ERROR_COLORS[0], linewidth=0.75, label="ITD error, left"),
        Line2D([], [], color=ITD_ERROR_COLORS[1], linewidth=0.75, label="ITD error, right"),
        Line2D([], [], color=RAW_ERROR_COLORS[0], linestyle="--", linewidth=0.75, label="Original-delay error, left"),
        Line2D([], [], color=RAW_ERROR_COLORS[1], linestyle="--", linewidth=0.75, label="Original-delay error, right"),
    )
    axis.legend(handles=handles, loc="center", ncols=3, frameon=False, fontsize=8)
    return figure


def main():
    parser = ArgumentParser(description="Plot measured and ERA-reconstructed FABIAN responses.")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    with np.load(RESULTS) as results:
        figures = (
            plot_time(results["measured"], results["itd_reconstructed"]),
            plot_frequency(results["measured"], results["raw_reconstructed"], results["itd_reconstructed"]),
        )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for figure, output in zip(figures, OUTPUTS[:-1]):
        figure.savefig(output, bbox_inches="tight", pad_inches=0.02)
    legend = plot_legend()
    legend.savefig(OUTPUTS[-1], bbox_inches="tight", pad_inches=0)
    if not args.no_show:
        plt.show()
    for figure in figures:
        plt.close(figure)
    plt.close(legend)


if __name__ == "__main__":
    main()
