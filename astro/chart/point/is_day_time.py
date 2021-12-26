from typing import Dict

from astro.schema import PointSchema
from astro.util import Point


def calculate_is_day_time(points: Dict[Point, PointSchema]) -> bool:
    """
    Returns whether the current points are during the day by looking if the sun is below the horizon.

    :param points: The current collection of calculated points.

    :return: Whether these points are found at day time.
    """
    if Point.sun not in points or Point.ascendant not in points:
        return True

    sun, asc = points[Point.sun], points[Point.ascendant]
    positive_difference_in_degrees = (sun.longitude - asc.longitude) % 360

    return positive_difference_in_degrees > 180
