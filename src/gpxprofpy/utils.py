"""
GPX profile plotter segments
"""

import numpy as np


def calculate_distance(latitude: np.ndarray, longitude: np.ndarray) -> np.ndarray:
    """Calculates distance from start and stores it in a numpy array"""

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
    """(TESTED) - Calculate slope from distance and elevation"""

    slope = np.zeros(distance.shape)

    for i, (dist, ele) in enumerate(zip(distance[1:], elevation[1:])):
        slope[i + 1] = slope_between_points(distance[i], elevation[i], dist, ele)

    return slope


def slope_between_points(dist1: float, ele1: float, dist2: float, ele2: float) -> float:
    """(TESTED) - Calculate slope in % between 2 points"""
    try:
        delta_dist = dist2 - dist1
        delta_ele = ele2 - ele1
        if delta_dist > 0:
            return 0.1 * delta_ele / delta_dist
    except TypeError:
        return None

    return 0


def get_slope_sign(slope: np.ndarray) -> list[int]:
    """(TESTED) - Returns slope sign"""

    slope_pos = slope > 0
    slope_neg = slope < 0

    return [int(1 * sp + -1 * sn) for sp, sn in zip(slope_pos, slope_neg)]

def find_closest_elevation(distance: np.ndarray, elevation: np.ndarray, target_distance: float):
    """Find elevation of closest point to distance in profile"""

    elevation_sup = elevation[distance >= target_distance]
    if len(elevation_sup) > 0:
        return elevation_sup[0]

    return elevation[-1]
