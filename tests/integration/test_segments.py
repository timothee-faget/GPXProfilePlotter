"""segments test module"""

import unittest

import numpy as np

from gpxprofpy.segments import (
    get_all_slope_segments,
    find_first_positive_mergeable_segment,
    find_first_negative_mergeable_segment,
    merge_segments,
    #TODO merge_positive_segments,
    #TODO merge_negative_segments,
    merge_three_segments,
    get_real_slope_segments,
    get_real_positive_slope_segments,
)

from gpxprofpy.utils import (
    calculate_slope,
)


class TestSegments(unittest.TestCase):
    """Segments test class"""

    def setUp(self):
        self.distance = np.array([0, 1, 2.5, 3, 4, 4.5, 5, 6.5, 7, 7.5, 9])
        self.elevation = np.array([0, 100, 120, 120, 70, 75, 40, 45, 44, 55, 60])
        self.segments = get_all_slope_segments(
            self.distance,
            self.elevation,
            calculate_slope(self.distance, self.elevation),
        )

    def test_get_all_slope_segments(self):
        """test extract_segments"""

        self.assertEqual(len(self.segments), 8)
        self.assertEqual(self.segments[0].get_size(), 2.5)
        self.assertEqual(self.segments[-1].get_size(), 2)
        np.testing.assert_almost_equal(self.segments[0].mean_slope(), 4.8, 2)
        np.testing.assert_almost_equal(self.segments[-1].mean_slope(), 0.8, 2)

    def test_find_first_positive_mergeable_segment(self):
        """test find_first_positive_mergeable_segment"""

        self.assertEqual(find_first_positive_mergeable_segment(self.segments, 0.9), 3)
        self.assertEqual(
            find_first_positive_mergeable_segment(self.segments[0:5], 0.9), None
        )

    def test_find_first_negative_mergeable_segment(self):
        """test find_first_negative_mergeable_segment"""

        self.assertEqual(find_first_negative_mergeable_segment(self.segments, 0.9), 2)
        self.assertEqual(
            find_first_negative_mergeable_segment(self.segments[5:-1], 0.9), None
        )

    def test_merge_segments(self):
        """test merge_segments"""

        merged_segments = merge_segments(self.segments, 0.9)

        self.assertEqual(len(merged_segments), 4)
        self.assertEqual(merged_segments[0].get_size(), 2.5)
        self.assertEqual(merged_segments[-1].get_size(), 5)
        np.testing.assert_almost_equal(merged_segments[0].mean_slope(), 4.8, 2)
        np.testing.assert_almost_equal(merged_segments[-1].mean_slope(), -0.2, 2)

    def test_merge_three_segments(self):
        """test merge_three_segments"""

        self.assertEqual(len(merge_three_segments(self.segments, 0)), 6)
        self.assertEqual(merge_three_segments(self.segments, 0)[0].get_size(), 5)
        self.assertEqual(merge_three_segments(self.segments, 0)[-1].get_size(), 2)
        np.testing.assert_almost_equal(
            merge_three_segments(self.segments, 0)[0].mean_slope(), 0.63, 2
        )
        np.testing.assert_almost_equal(
            merge_three_segments(self.segments, 0)[-1].mean_slope(), 0.8, 2
        )

    def test_get_real_slope_segments(self):
        """test get_real_slope_segments"""

        real_segments = get_real_slope_segments(
            self.distance, self.elevation, threshold=0.9
        )

        self.assertEqual(len(real_segments), 4)
        self.assertEqual(real_segments[0].get_size(), 2.5)
        self.assertEqual(real_segments[-1].get_size(), 5)
        np.testing.assert_almost_equal(real_segments[0].mean_slope(), 4.8, 2)
        np.testing.assert_almost_equal(real_segments[-1].mean_slope(), -0.2, 2)

    def test_get_real_positive_slope_segments(self):
        """test get_real_positive_slope_segments"""

        positive_segments = get_real_positive_slope_segments(
            self.distance, self.elevation, threshold=0.9, merge_threshold=0.9
        )

        self.assertEqual(len(positive_segments), 2)
        self.assertEqual(positive_segments[0].get_size(), 2.5)
        self.assertEqual(positive_segments[-1].get_size(), 5)
        np.testing.assert_almost_equal(positive_segments[0].mean_slope(), 4.8, 2)
        np.testing.assert_almost_equal(positive_segments[-1].mean_slope(), -0.2, 2)
