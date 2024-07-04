"""
GPX profile plotter segments
"""

from dataclasses import dataclass

import csv

# import numpy as np
import matplotlib.axes as axs

from . import utils, params
from . import profile as prf


@dataclass
class RemarquablePoint:
    """Remarquable points"""

    distance: float
    label: str
    has_water: bool

    def get_text(self, max_distance: float) -> str:
        """Gets label text"""
        prefix = ""
        if self.distance == 0:
            prefix = "Dép "
        elif self.distance > max_distance:
            prefix = "Arr "

        suffix = ""
        if self.has_water:
            suffix += " E"

        return f"{prefix}{int(self.distance)} - {self.label}{suffix}"

    def get_color(self, max_distance):
        """Gets color according to position"""

        if self.distance == 0:
            return params.COLOR_START
        if self.distance > max_distance:
            return params.COLOR_FINISH
        return params.COLOR_POINT

    def get_fontweight(self, max_distance):
        """Gets fontweight according to position"""

        if self.distance == 0 or self.distance > max_distance:
            return "bold"
        return "normal"


def read_remarquable_points_file(filename: str) -> list[RemarquablePoint]:
    """reads remarquable points in csv file"""

    remarquable_points = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lines = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for dist, label, water_point in lines:
            water_point = True if int(water_point) == 1 else False
            remarquable_points.append(RemarquablePoint(float(dist), label, water_point))

    return remarquable_points

def plot_remarquable_points(ax: axs.Axes, profile: prf.GPXProfile):
    """Plots remarquable points at their respective distances"""
    max_distance = int(profile.max_distance())

    remarquable_points = read_remarquable_points_file(f"{profile.name}.csv")

    for rem_pt in remarquable_points:
        elevation = (
            utils.find_closest_elevation(
                profile.distance, profile.elevation, rem_pt.distance
            )
            + 300
        )
        plot_remarquables_point(
            ax,
            rem_pt,
            elevation,
            max_distance,
        )


def plot_remarquables_point(
    ax: axs.Axes, point: RemarquablePoint, elevation: float, max_distance: float
):
    """Plots a remarquable point"""

    ax.vlines(
        point.distance,
        0,
        elevation,
        colors=point.get_color(max_distance),
        linestyles="--",
        zorder=200,
    )
    ax.text(
        point.distance - 3,
        elevation + 100,
        point.get_text(max_distance),
        color=point.get_color(max_distance),
        fontweight=point.get_fontweight(max_distance),
        rotation=90,
        zorder=200,
    )
