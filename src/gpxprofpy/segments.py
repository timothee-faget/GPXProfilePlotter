"""
GPX profile plotter segments
"""

from dataclasses import dataclass

import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.axes as axs

from . import utils, params


@dataclass
class SlopeSegment:
    """(TESTED) - Defines a slope segment"""

    distance: np.ndarray
    elevation: np.ndarray
    slope: np.ndarray
    sign: int

    def __add__(self, segment2):
        return SlopeSegment(
            np.concatenate([self.distance, segment2.distance[1:]]),
            np.concatenate([self.elevation, segment2.elevation[1:]]),
            np.concatenate([self.slope, segment2.slope[1:]]),
            self.sign,
        )

    def __repr__(self):
        return f"SlopeSegment: {self.get_size()}km, pente moyenne: {self.mean_slope()}%"

    def get_size(self):
        """return size of segment, in km"""
        return self.distance[-1] - self.distance[0]

    def get_distance_deltas(self):
        """return array of distance between segment points"""
        return np.array(
            [0] + [d - self.distance[i] for i, d in enumerate(self.distance[1:])]
        )

    def mean_slope(self):
        """return mean slope"""
        return np.round(np.average(self.slope, weights=self.get_distance_deltas()), 2)


def get_real_positive_slope_segments(
    distance: np.ndarray,
    elevation: np.ndarray,
    threshold: float = params.SEUIL,
    merge_threshold: float = params.SEUIL,
):
    """(TESTED) - Gets positive slope segments"""

    segments = get_real_slope_segments(distance, elevation, threshold=merge_threshold)

    return [seg for seg in segments if seg.sign == 1 and seg.get_size() > threshold]


def get_real_slope_segments(
    distance: np.ndarray, elevation: np.ndarray, threshold: float = params.SEUIL_MERGE
):
    """(TESTED) - Gets slope segments cleaned"""

    slope = utils.calculate_slope(distance, elevation)
    segments = get_all_slope_segments(distance, elevation, slope)

    return merge_segments(segments, threshold)


def get_all_slope_segments(
    distance: np.ndarray, elevation: np.ndarray, slope: np.ndarray
) -> list[SlopeSegment]:
    """(TESTED) - Find all slope segments"""

    slope = utils.calculate_slope(distance, elevation)
    slope_sign = utils.get_slope_sign(slope)

    segments_ends, segments_signs = get_segments_end_indexes(slope_sign)
    return extract_segments(distance, elevation, slope, segments_ends, segments_signs)


def get_segments_end_indexes(slope_sign: list[int]) -> tuple[list[int], list[int]]:
    """(TESTED) - Return indexes of segments ends and their signs"""

    segments_ends, segments_sign = [], []
    for i, sg in enumerate(slope_sign[1:]):
        try:
            if (sg * slope_sign[i + 2]) <= 0 and sg != slope_sign[i + 2]:
                segments_ends.append(i + 1)
                segments_sign.append(sg)
        except IndexError:
            if sg != slope_sign[i]:
                segments_ends.append(i + 1)
                segments_sign.append(sg)

    if segments_ends[-1] != len(slope_sign) - 1:
        segments_ends.append(len(slope_sign) - 1)
        segments_sign.append(slope_sign[-1])

    return segments_ends, segments_sign


def extract_segments(
    distance: np.ndarray,
    elevation: np.ndarray,
    slope: np.ndarray,
    indexes: list[int],
    signs: list[int],
) -> list[SlopeSegment]:
    """(TESTED) - Extract segments from their end indexes"""

    segments = []
    for i, (index, sign) in enumerate(zip(indexes, signs)):
        if i == 0:
            segments.append(
                SlopeSegment(
                    distance[0 : index + 1],
                    elevation[0 : index + 1],
                    slope[0 : index + 1],
                    sign,
                )
            )
        else:
            segments.append(
                SlopeSegment(
                    distance[indexes[i - 1] : index + 1],
                    elevation[indexes[i - 1] : index + 1],
                    slope[indexes[i - 1] : index + 1],
                    sign,
                )
            )

    return segments


def merge_segments(
    segments: list[SlopeSegment], threshold: float
) -> list[SlopeSegment]:
    """(TESTED) - merges slope segments that need it"""

    segments = merge_negative_segments(segments, threshold)
    segments = merge_positive_segments(segments, threshold)
    segments = merge_negative_segments(segments, threshold)

    return segments


def merge_positive_segments(
    segments: list[SlopeSegment], threshold: float
) -> list[SlopeSegment]:
    """Merges positive slope segments that need it"""

    seg_to_merge = find_first_positive_mergeable_segment(segments, threshold)
    max_iteration = 2 * len(segments)
    iteration = 0
    while seg_to_merge is not None and iteration < max_iteration:
        iteration += 1
        segments = merge_three_segments(segments, seg_to_merge)
        seg_to_merge = find_first_positive_mergeable_segment(segments, threshold)

    return segments


def merge_negative_segments(
    segments: list[SlopeSegment], threshold: float
) -> list[SlopeSegment]:
    """Merges negative slope segments that need it"""

    seg_to_merge = find_first_negative_mergeable_segment(segments, threshold)
    max_iteration = 2 * len(segments)
    iteration = 0
    while seg_to_merge is not None and iteration < max_iteration:
        iteration += 1
        segments = merge_three_segments(segments, seg_to_merge)
        seg_to_merge = find_first_negative_mergeable_segment(segments, threshold)

    return segments


def merge_three_segments(
    segments: list[SlopeSegment], index: int
) -> list[SlopeSegment]:
    """(TESTED) - Merge next 3 segments from index"""

    try:
        new_segment = segments[index] + segments[index + 1] + segments[index + 2]
        segments[index] = new_segment
        segments.pop(index + 2)
        segments.pop(index + 1)
    except IndexError:
        pass

    return segments


def find_first_positive_mergeable_segment(
    segments: list[SlopeSegment], threshold: float
) -> int | None:
    """(TESTED) - Find the first positive segment whose next segment is shorter than a threshold"""

    for i, seg in enumerate(segments):
        try:
            if (
                seg.sign == 1
                and segments[i + 1].get_size() < threshold
                and segments[i + 2].sign == 1
            ) or (
                seg.sign == 1
                and segments[i + 1].get_size() + segments[i + 2].get_size() < threshold
                and segments[i + 3].sign == 1
            ):
                return i
        except IndexError:
            pass
    return None


def find_first_negative_mergeable_segment(
    segments: list[SlopeSegment], threshold: float
) -> int | None:
    """(TESTED) - Find the first negative segment whose next segment is shorter than a threshold"""

    for i, seg in enumerate(segments):
        try:
            if (
                seg.sign == -1
                and segments[i + 1].get_size() < threshold
                and segments[i + 2].sign == -1
            ) or (
                seg.sign == -1
                and segments[i + 1].get_size() + segments[i + 2].get_size() < threshold
                and segments[i + 3].sign == -1
            ):
                return i
        except IndexError:
            pass
    return None


def fill_under_segments(
    ax: axs.Axes, slope_segments: list[SlopeSegment]
) -> None:
    """Fill color according to mean slope under all positive slope segments"""

    for seg in slope_segments:
        slope_color = get_slope_color(seg.mean_slope())
        ax.fill_between(seg.distance, seg.elevation, 0, color=slope_color, zorder=10)


def fill_under_all_segments(
    ax: axs.Axes, slope_segments: list[SlopeSegment]
) -> None:
    """FOR DEBUG ONLY - Fill color under all slope segments"""

    i = 0
    colors = ["#353535", "#E445E4"]
    for seg in slope_segments:
        ax.fill_between(seg.distance, seg.elevation, 0, color=colors[i], zorder=10)
        i = 1 if i == 0 else 0


def get_slope_color(mean_slope: float) -> str:
    """Gets color according to mean slope"""

    normalized_slope = int(mean_slope / 2)

    if normalized_slope > len(params.COLORS_SLOPE) - 1:
        return params.COLORS_SLOPE[-1]

    return params.COLORS_SLOPE[normalized_slope]
