"""
GPX profile plotter segments
"""

from dataclasses import dataclass

import numpy as np
import gpxpy as gp

from . import utils


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


def read_gpx_file(gpx_filename: str) -> GPXProfile:
    """Read GPX file and return the profile data"""

    name = gpx_filename.replace(".gpx", "")  # Get GPX name
    latitude, longitude, elevation = extract_data(
        gpx_filename
    )  # Extract latitude, longitude and elevation
    distance = utils.calculate_distance(
        latitude, longitude
    )  # Convert latitude and longitude to distance
    slope = utils.calculate_slope(distance, elevation)  # Calculate slope

    return GPXProfile(name, distance, elevation, slope)


def extract_data(gpx_filename: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Extracts latitude, longitude and elevation from file"""

    with open(gpx_filename, encoding="utf-8") as gpx_file:
        gpx_file_data = gp.parse(gpx_file)
    gpx_points = gpx_file_data.tracks[0].segments[0].points
    latitude = np.array([pt.latitude for pt in gpx_points])
    longitude = np.array([pt.longitude for pt in gpx_points])
    elevation = np.array([pt.elevation for pt in gpx_points])

    return (latitude, longitude, elevation)
