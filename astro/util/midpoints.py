from typing import List

from astro.util import Point


def calculate_midpoints(points: List[Point]):
    """
    Returns a list of all points between the given points.

    :param points: The points to calculate midpoints between.

    :return: The midpoints.
    """
    midpoints = []
    other_points = points[1:]

    for from_point in points:
        for to_point in other_points:
            midpoints.append({"from_point": from_point, "to_point": to_point})

        other_points = other_points[1:]

    return midpoints
