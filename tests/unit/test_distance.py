"""slope functions test module"""

import unittest

import numpy as np

from gpxprofpy.utils import distance_between_points, calculate_distance


class TestDistanceFunctions(unittest.TestCase):
    """Distance functions test class"""

    def setUp(self):
        self.lat = np.array([0, 57.3, -57.3])
        self.lon = np.array([0, 57.3, -171.9])

    def test_distance_between_points_1(self):
        """test distance_between_points 1"""
        np.testing.assert_almost_equal(distance_between_points(0, 0, 1, 1), 8120, 0)

    def test_distance_between_points_2(self):
        """test distance_between_points 2"""
        np.testing.assert_almost_equal(distance_between_points(1, 1, -1, -3), 17125, 0)

    def test_calculate_distance(self):
        """tes calculate distance"""
        np.testing.assert_almost_equal(calculate_distance(self.lat, self.lon), [0, 8120, 25245], 0)


if __name__ == "__main__":
    unittest.main()
