"""
GPX profile plotter functions and classes
"""

from dataclasses import dataclass

import csv

import numpy as np
import gpxpy as gp
import matplotlib.pyplot as plt
import matplotlib.axes as axs

from . import params


@dataclass
class GPXProfile:
    """Gathers data from GPX Profile"""

    name: str
    distance: np.ndarray
    elevation: np.ndarray
    slope: np.ndarray

    def max_distance(self) -> float:
        """Returns max distance of profile"""
        return np.max(self.distance)

    def max_elevation(self) -> float:
        """Returns max elevation of profile"""
        return np.max(self.elevation)

    def plot(
        self,
        plot_slope: bool = False,
        plot_points: bool = False,
        save_fig: bool = False,
    ) -> None:
        """Plots profile"""
        plot_profile(self, plot_slope, plot_points, save_fig)


@dataclass
class GPXFile:
    """Represent a GPX File"""

    filename: str

    def csv_name(self) -> str:
        """Return associated"""
        return self.filename.replace(".gpx", ".csv")

    def profile(self) -> GPXProfile:
        """Extract data from GPX and stores it in a GPXProfile object"""
        return read_gpx_file(self.filename)


@dataclass
class SlopeSegment:
    """Slope segment data"""

    distance: np.ndarray
    elevation: np.ndarray
    slope: np.ndarray

    def mean_slope(self) -> float:
        """Return mean slope"""
        return np.mean(self.slope)


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


def plot_profile(
    profile: GPXProfile, plot_slope: bool, plot_points: bool, save_fig: bool
) -> None:
    """Plots GPX elevation profile"""

    fig, ax = plt.subplots(figsize=(14, 3), layout="constrained")

    fill_under_profile(ax, profile.distance, profile.elevation)

    if plot_slope:
        slope_segments = get_slope_segments(profile, params.SEUIL)
        fill_under_segments(ax, slope_segments)

    if plot_points:
        try:
            plot_remaquable_points(ax, profile)
        except FileNotFoundError:
            print("No CSV file found...")

    remove_axes_frame(ax)
    set_axes_limits(ax, profile)
    set_grid(ax)

    ax.plot(profile.distance, profile.elevation, color=params.COLOR_PROFILE, zorder=100)

    if save_fig:
        fig.savefig(f"{profile.name}.png", dpi=350)

    plt.show()


def read_gpx_file(gpx_filename: str) -> GPXProfile:
    """Read GPX file and retrun the profile data"""

    name = gpx_filename.replace(".gpx", "")  # Get GPX name
    latitude, longitude, elevation = extract_data(
        gpx_filename
    )  # Extract latitude, longitude and elevation
    distance = calculate_distance(
        latitude, longitude
    )  # Convert latitude and longitude to distance
    slope = calculate_slope(distance, elevation)  # Calculate slope

    return GPXProfile(name, distance, elevation, slope)


def extract_data(gpx_filename: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Extracts latitude, longitude and elevation from file"""

    with open(gpx_filename, encoding="utf-8") as gpx_file:
        gpx_file_data = gp.parse(gpx_file)
    points = gpx_file_data.tracks[0].segments[0].points
    latitude = np.array([pt.latitude for pt in points])
    longitude = np.array([pt.longitude for pt in points])
    elevation = np.array([pt.elevation for pt in points])

    return (latitude, longitude, elevation)


def calculate_distance(latitude: np.ndarray, longitude: np.ndarray) -> np.ndarray:
    """Calcultaes distance from start and stores it in a numpy array"""

    distance = np.zeros(latitude.shape)
    latitude_rad = np.radians(latitude)
    longitude_rad = np.radians(longitude)
    for i, (lat, lon) in enumerate(zip(latitude_rad[1:], longitude_rad[1:])):
        distance[i + 1] = distance[i] + distance_between_points(
            latitude_rad[i], longitude_rad[i], lat, lon
        )

    return distance


def distance_between_points(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Calculate distance between 2 GPS points from their latitudes and longitudes, in radians"""

    return 6371 * np.acos(
        min(
            np.sin(lat1) * np.sin(lat2)
            + np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1),
            1,
        )
    )


def calculate_slope(distance: np.ndarray, elevation: np.ndarray) -> np.ndarray:
    """Calculate slope from distance and elevation"""

    slope = np.zeros(distance.shape)

    for i, (dist, ele) in enumerate(zip(distance[1:], elevation[1:])):
        slope[i + 1] = slope_between_points(distance[i], elevation[i], dist, ele)

    return slope


def slope_between_points(dist1: float, ele1: float, dist2: float, ele2: float) -> float:
    """Calculate slope in % between 2 points"""
    delta_dist = dist2 - dist1
    delta_ele = ele2 - ele1
    if delta_dist > 0:
        return 0.1 * delta_ele / delta_dist

    return 0


def fill_under_profile(
    ax: axs.Axes, distance: np.ndarray, elevation: np.ndarray
) -> None:
    """Fills all under profile"""

    ax.fill_between(distance, elevation, 0, color=params.COLOR_FILL, zorder=5)


def get_slope_segments(profile: GPXProfile, seuil: float) -> list[SlopeSegment]:
    """Get all positive slope segments that are longer than seuil"""

    slope_pos = profile.slope > 0
    is_slope_pos, deb = False, 0
    slope_segments = []
    for i, sp in enumerate(slope_pos):
        if not sp and is_slope_pos:
            is_slope_pos = False
            if (profile.distance[i] - profile.distance[deb]) > seuil:
                slope_segments.append(
                    SlopeSegment(
                        profile.distance[deb:i],
                        profile.elevation[deb:i],
                        profile.slope[deb:i],
                    )
                )
        elif sp and not is_slope_pos:
            is_slope_pos = True
            deb = i

    return slope_segments


def fill_under_segments(ax: axs.Axes, slope_segments: list[SlopeSegment]) -> None:
    """Fill color according to mean slope under all slope segments"""

    for seg in slope_segments:
        slope_color = get_slope_color(seg.mean_slope())
        ax.fill_between(seg.distance, seg.elevation, 0, color=slope_color, zorder=10)


def get_slope_color(mean_slope: float) -> str:
    """Gets color according to mean slope"""

    normalized_slope = int(mean_slope / 2)

    if normalized_slope > len(params.COLORS_SLOPE) - 1:
        return params.COLORS_SLOPE[-1]

    return params.COLORS_SLOPE[normalized_slope]


def read_remarquable_points_file(filename: str) -> list[RemarquablePoint]:
    """reads remarquable points in csv file"""

    remarquable_points = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        lines = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for dist, label, water_point in lines:
            water_point = True if int(water_point) == 1 else False
            remarquable_points.append(RemarquablePoint(float(dist), label, water_point))

    return remarquable_points


def plot_remaquable_points(ax: axs.Axes, profile: GPXProfile):
    """Plots remarquable points at their respective distances"""
    max_distance = int(profile.max_distance())

    remarquable_points = read_remarquable_points_file(f"{profile.name}.csv")

    for rem_pt in remarquable_points:
        elevation = find_closest_elevation(profile, rem_pt.distance) + 300
        point_remaquables_point(
            ax,
            rem_pt,
            elevation,
            max_distance,
        )


def find_closest_elevation(profile: GPXProfile, distance: float):
    """Find elevation of closest point to distance in profile"""

    elevation_sup = profile.elevation[profile.distance >= distance]
    if len(elevation_sup) > 0:
        return elevation_sup[0]

    return profile.elevation[-1]


def point_remaquables_point(
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


def remove_axes_frame(ax: axs.Axes) -> None:
    """Removes axes frame"""

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def set_axes_limits(ax: axs.Axes, profile: GPXProfile) -> None:
    """Sets axes limits according to profile"""
    ax.set_ylim((0, profile.max_elevation() * 2.5))
    ax.set_xlim((-5, profile.max_distance() + 5))


def set_grid(ax: axs.Axes) -> None:
    """Sets grid"""
    ax.grid(axis="y", linestyle="--", zorder=0, color=params.COLOR_GRID)
