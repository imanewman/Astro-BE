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

    - Determines whether the chart is during the day.

    :param points: The current collection of calculated points.
    :param is_day_time: Whether this chart is during the day.

    :return: The calculated chart summary.
    """
    if Point.sun not in points or Point.moon not in points or Point.ascendant not in points:
        # Return an empty summary if the big 3 points are not all calculated.
        return SummarySchema()

    sun, moon, asc = points[Point.sun], points[Point.moon], points[Point.ascendant]

    return SummarySchema(
        is_day_time=is_day_time,
        sun=sun.sign, moon=moon.sign, asc=asc.sign,
    )
