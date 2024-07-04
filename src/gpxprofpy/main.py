"""
GPX profile plotter functions and classes
"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.axes as axs

from . import params, segments, points
from . import profile as prf


def plot_profile(
    profile: prf.GPXProfile, plot_slope: bool, plot_points: bool, save_fig: bool
) -> None:
    """Plots GPX elevation profile"""

    fig, ax = plt.subplots(figsize=(14, 3), layout="constrained")

    fill_under_profile(ax, profile.distance, profile.elevation)

    if plot_slope:
        slope_segments = segments.get_real_positive_slope_segments(
            profile.distance, profile.elevation
        )
        segments.fill_under_segments(ax, slope_segments)

    if plot_points:
        try:
            points.plot_remarquable_points(ax, profile)
        except FileNotFoundError:
            print("No CSV file found...")

    remove_axes_frame(ax)
    set_axes_limits(ax, profile)
    set_grid(ax)

    ax.plot(profile.distance, profile.elevation, color=params.COLOR_PROFILE, zorder=100)

    if save_fig:
        fig.savefig(f"{profile.name}.png", dpi=350)

    plt.show()


def fill_under_profile(
    ax: axs.Axes, distance: np.ndarray, elevation: np.ndarray
) -> None:
    """Fills all under profile"""

    ax.fill_between(distance, elevation, 0, color=params.COLOR_FILL, zorder=5)


def remove_axes_frame(ax: axs.Axes) -> None:
    """Removes axes frame"""

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def set_axes_limits(ax: axs.Axes, profile: prf.GPXProfile) -> None:
    """Sets axes limits according to profile"""
    ax.set_ylim((0, profile.max_elevation() * 2.5))
    ax.set_xlim((-5, profile.max_distance() + 5))


def set_grid(ax: axs.Axes) -> None:
    """Sets grid"""
    ax.grid(axis="y", linestyle="--", zorder=0, color=params.COLOR_GRID)
