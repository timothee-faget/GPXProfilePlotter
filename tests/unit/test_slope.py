"""slope functions test module"""

import unittest

import numpy as np

from gpxprofpy.utils import slope_between_points, calculate_slope, get_slope_sign


class TestSlopeFunctions(unittest.TestCase):
    """Slope functions test class"""

    def setUp(self):
        self.distance_1 = np.array([0, 1, 2.5, 3, 4, 5, 6.5, 7, 7.5, 9])
        self.elevation_1 = np.array([0, 100, 120, 120, 70, 40, 45, 44, 55, 60])
        self.slope_1 = np.array([0, 10, 1.33, 0, -5, -3, 0.33, -0.2, 2.2, 0.33])

        self.distance_2 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.elevation_2 = np.array([0, 100, 200, 300, 400, 500, 400, 300, 200, 100, 0])
        self.slope_2 = np.array([0, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10])

    def test_slope_between_points_1(self):
        """test slope_between_points 1"""
        self.assertEqual(slope_between_points(0, 0, 1, 100), 10)

    def test_slope_between_points_2(self):
        """test slope_between_points 2"""
        self.assertEqual(slope_between_points(1, 100, 2, 100), 0)

    def test_slope_between_points_3(self):
        """test slope_between_points 3"""
        self.assertEqual(slope_between_points(0, 100, 1, 0), -10)

    def test_slope_between_points_4(self):
        """test slope_between_points 4"""
        self.assertEqual(slope_between_points(0, 0, 1, -200), -20)

    def test_slope_between_points_5(self):
        """test slope_between_points 5"""
        self.assertRaises(TypeError, slope_between_points(0, 0, 1, "ahaa"))

    def test_calculate_slope_1(self):
        """test calculate_slope 1"""
        np.testing.assert_almost_equal(
            calculate_slope(self.distance_1, self.elevation_1), self.slope_1, 2
        )

    def test_calculate_slope_2(self):
        """test calculate_slope 2"""
        np.testing.assert_almost_equal(
            calculate_slope(self.distance_2, self.elevation_2), self.slope_2, 2
        )

    def test_slope_sign_1(self):
        """test get_slope_sign 1"""
        np.testing.assert_equal(
            get_slope_sign(self.slope_1), np.array([0, 1, 1, 0, -1, -1, 1, -1, 1, 1])
        )

    def test_slope_sign_2(self):
        """test get_slope_sign 2"""
        np.testing.assert_equal(
            get_slope_sign(self.slope_2),
            np.array([0, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]),
        )


if __name__ == "__main__":
    unittest.main()
