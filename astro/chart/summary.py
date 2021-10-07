from typing import Dict

from astro.util import Point
from astro.schema import SummarySchema, PointSchema


def create_summary(
        points: Dict[Point, PointSchema],
        is_day_time: bool
) -> SummarySchema:
    """
    Creates a summary of the calculated points.

    - Requires that planetary conditions have been calculated.

    - Finds the sign of the sun, moon, and ascendant.
    - Finds the planet that rules the ascendant.
    - Determines whether the chart is during the day.

    :param points: The current collection of calculated points.
    :param is_day_time: Whether this chart is during the day.

    :return: The calculated chart summary.
    """

    # Return an empty summary if the big 3 points are not all calculated
    if Point.sun not in points or Point.moon not in points or Point.ascendant not in points:
        return SummarySchema()

    sun, moon, asc = points[Point.sun], points[Point.moon], points[Point.ascendant]

    return SummarySchema(
        is_day_time=is_day_time,
        sun=sun.sign, moon=moon.sign, asc=asc.sign,
        asc_ruler_sign=asc.rulers.sign,
        asc_ruler_bound=asc.rulers.bound,
        asc_ruler_decan=asc.rulers.decan,
    )


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
