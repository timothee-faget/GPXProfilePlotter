"""segments functions test module"""

import unittest

import numpy as np

from gpxprofpy.segments import (
    SlopeSegment,
    get_segments_end_indexes,
    extract_segments,
    get_all_slope_segments,
)

from gpxprofpy.utils import (
    calculate_slope,
    get_slope_sign,
)


class TestSegmentsFunctions(unittest.TestCase):
    """Segments functions test class"""

    def setUp(self):
        self.distance = np.array([0, 1, 2.5, 3, 4, 5, 6.5, 7, 7.5, 9])
        self.elevation = np.array([0, 100, 120, 120, 70, 40, 45, 44, 55, 60])

    def test_segments(self):
        """test segments"""
        distance = np.array([0, 1, 2.5])
        elevation = np.array([0, 50, 100])
        slope = calculate_slope(distance, elevation)
        segment = SlopeSegment(distance, elevation, slope, 1)
        self.assertEqual(segment.get_size(), 2.5)
        np.testing.assert_equal(
            segment.get_distance_deltas(),
            np.array([0, 1, 1.5]),
        )
        self.assertEqual(segment.mean_slope(), 4)

    def test_segment_end_indexes(self):
        """test get_segments_end_indexes"""
        slope = calculate_slope(self.distance, self.elevation)
        slope_sign = get_slope_sign(slope)

        segment_end_indexes, segment_signs = get_segments_end_indexes(slope_sign)
        self.assertEqual(segment_end_indexes, [2, 3, 5, 6, 7, 9])
        self.assertEqual(segment_signs, [1, 0, -1, 1, -1, 1])

    def test_segment_end_indexes_flat(self):
        """test get_segments_end_indexes"""
        distance = np.array([0, 1, 2, 3, 4])
        elevation = np.array([0, 10, 10, 10, 0])
        slope = calculate_slope(distance, elevation)
        slope_sign = get_slope_sign(slope)

        segment_end_indexes, segment_signs = get_segments_end_indexes(slope_sign)
        self.assertEqual(segment_end_indexes, [1, 3, 4])
        self.assertEqual(segment_signs, [1, 0, -1])

    def test_extract_segments(self):
        """test extract_segments"""
        slope = calculate_slope(self.distance, self.elevation)
        slope_sign = get_slope_sign(slope)
        segment_end_indexes, segment_signs = get_segments_end_indexes(slope_sign)
        segments = extract_segments(
            self.distance, self.elevation, slope, segment_end_indexes, segment_signs
        )
        self.assertEqual(len(segments), 6)
        self.assertEqual(segments[0].get_size(), 2.5)
        self.assertEqual(segments[-1].get_size(), 2)
        np.testing.assert_almost_equal(segments[0].mean_slope(), 4.8, 2)
        np.testing.assert_almost_equal(segments[-1].mean_slope(), 0.8, 2)

    def test_get_all_slope_segments(self):
        """test extract_segments"""
        slope = calculate_slope(self.distance, self.elevation)
        segments = get_all_slope_segments(self.distance, self.elevation, slope)
        self.assertEqual(len(segments), 6)
        self.assertEqual(segments[0].get_size(), 2.5)
        self.assertEqual(segments[-1].get_size(), 2)
        np.testing.assert_almost_equal(segments[0].mean_slope(), 4.8, 2)
        np.testing.assert_almost_equal(segments[-1].mean_slope(), 0.8, 2)
