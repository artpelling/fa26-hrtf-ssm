"""Plot theoretical economy-SVD memory and work for projected ERA."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from src.plotting import PAPER_FIGURE_SIZE, golden_axes, plot_color


OUTPUT = Path("generated/figures/scalability.pdf")
LEGEND = OUTPUT.with_name("scalability-legend.pdf")
N_DIRECTIONS = 11_950
N_SAMPLES = 255
N_EARS = 2
FLOAT_BYTES = 8
N_ROWS = N_EARS * N_SAMPLES
MAX_VIRTUAL_INPUTS = N_ROWS


def svd_costs(n_inputs):
    """Return economy-SVD storage and proportional full-SVD work.

    The storage includes the dense input Hankel matrix and economy-size left and
    right singular-vector factors, but excludes algorithm-specific workspace.
    """
    n_columns = N_SAMPLES * n_inputs
    memory_gib = FLOAT_BYTES * (2 * N_ROWS * n_columns + N_ROWS**2) / 2**30
    svd_work = N_ROWS**2 * n_columns
    return memory_gib, svd_work


def plot():
    """Plot direct and worst-case loss-free projected ERA scaling."""
    directions = np.arange(1, N_DIRECTIONS + 1)
    direct_memory, direct_work = svd_costs(directions)
    projected_inputs = np.minimum(directions, MAX_VIRTUAL_INPUTS)
    projected_memory, projected_work = svd_costs(projected_inputs)
    marker_indices = 2 ** np.arange(int(np.log2(N_DIRECTIONS)) + 1) - 1

    figure, memory_axis = plt.subplots(figsize=PAPER_FIGURE_SIZE, layout="constrained")
    work_axis = memory_axis.twinx()
    work_axis.set_zorder(memory_axis.get_zorder() - 1)
    memory_axis.patch.set_visible(False)
    work_axis.patch.set_visible(False)
    golden_axes(memory_axis)

    for axis, values, color, marker, linestyle, label in (
        (memory_axis, direct_memory, plot_color("memory"), "o", "-", "Direct ERA memory"),
        (memory_axis, projected_memory, plot_color("memory"), "x", "--", "Projected ERA memory"),
        (work_axis, direct_work, plot_color("work"), "s", "-", "Direct ERA work"),
        (work_axis, projected_work, plot_color("work"), "x", "--", "Projected ERA work"),
    ):
        axis.plot(
            directions,
            values,
            color=color,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor="none",
            markeredgewidth=1.2 if marker == "x" else 1,
            markevery=marker_indices,
            label=label,
        )

    memory_axis.axvline(MAX_VIRTUAL_INPUTS, color="tab:red", linewidth=0.8, zorder=0)

    memory_ticks = 10.0 ** np.arange(-3, 3)
    work_ticks = 10.0 ** np.arange(7, 13)
    memory_axis.set(
        xlabel="Number of sampled directions",
        ylabel="Memory (GiB)",
        xlim=(1, N_DIRECTIONS),
        xscale="log",
        yscale="log",
        ylim=(memory_ticks[0], memory_ticks[-1]),
        yticks=memory_ticks,
    )
    work_axis.set(
        ylabel="Work (FLOP)",
        yscale="log",
        ylim=(work_ticks[0], work_ticks[-1]),
        yticks=work_ticks,
    )
    memory_axis.tick_params(axis="y", which="both", left=True, labelleft=True)
    work_axis.tick_params(axis="y", which="both", right=True, labelright=True)
    memory_axis.yaxis.label.set_color(plot_color("memory"))
    work_axis.yaxis.label.set_color(plot_color("work"))
    memory_axis.grid(which="major", alpha=0.3)
    memory_axis.grid(which="minor", alpha=0.15, linewidth=0.5)
    memory_axis.minorticks_on()
    return figure


def plot_legend():
    """Create the compact external legend for the scalability figure."""
    figure, axis = plt.subplots(figsize=(PAPER_FIGURE_SIZE[0], 0.55), layout="constrained")
    axis.axis("off")
    curves = [
        Line2D([], [], color=plot_color("memory"), marker="o", markerfacecolor="none", label="Direct ERA memory"),
        Line2D([], [], color=plot_color("memory"), linestyle="--", marker="x", label="Projected ERA memory"),
        Line2D([], [], color=plot_color("work"), marker="s", markerfacecolor="none", label="Direct ERA work"),
        Line2D([], [], color=plot_color("work"), linestyle="--", marker="x", label="Projected ERA work"),
    ]
    axis.legend(handles=curves, loc="center", ncols=2, frameon=False, fontsize=9)
    return figure


def main():
    parser = ArgumentParser(description="Plot theoretical projected-ERA scaling.")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    figure = plot()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT, bbox_inches="tight", pad_inches=0.02)
    legend = plot_legend()
    legend.savefig(LEGEND, bbox_inches="tight", pad_inches=0)
    if not args.no_show:
        plt.show()
    plt.close(figure)
    plt.close(legend)


if __name__ == "__main__":
    main()
