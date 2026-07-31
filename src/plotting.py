"""Shared Matplotlib settings for paper figures."""

from math import sqrt

import matplotlib as mpl


COLOR_MAP = "tab20"
COLOR_CYCLE = mpl.colormaps[COLOR_MAP].colors
COLOR_FAMILIES = {
    "no_removal": (0, 1),
    "itd_removal": (2, 3),
    "left_ear": (4, 5),
    "right_ear": (6, 7),
    "memory": (8, 9),
    "work": (10, 11),
}


def plot_color(family, shade=0):
    """Return a dark (0) or light (1) color from the selected palette family."""
    return COLOR_CYCLE[COLOR_FAMILIES[family][shade]]


GOLDEN_RATIO = (1 + sqrt(5)) / 2
COLUMN_WIDTH_IN = 81 / 25.4  # 170 mm text width, two columns, 8 mm gutter.
PAPER_FIGURE_SIZE = (COLUMN_WIDTH_IN, COLUMN_WIDTH_IN)
HSV_FIGURE_SIZE = (COLUMN_WIDTH_IN, 2.0)
FONT_SIZE_PT = 10
DPI = 300
SELECTED_ORDER_MARKER_STYLE = {"color": "tab:red", "marker": "o", "markerfacecolor": "none"}

mpl.rcParams.update(
    {
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "font.family": "serif",
        "font.size": FONT_SIZE_PT,
        "axes.labelsize": FONT_SIZE_PT,
        "axes.titlesize": FONT_SIZE_PT,
        "axes.prop_cycle": mpl.cycler(color=COLOR_CYCLE),
        "legend.fontsize": FONT_SIZE_PT,
        "xtick.labelsize": FONT_SIZE_PT,
        "ytick.labelsize": FONT_SIZE_PT,
        "text.usetex": True,
    }
)


def golden_axes(axis):
    """Set the data area to the golden ratio, excluding decorations."""
    axis.set_box_aspect(1 / GOLDEN_RATIO)
