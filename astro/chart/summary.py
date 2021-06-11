from typing import Dict

from astro.util import Point, zodiac_sign_traits
from astro.schema import SummarySchema, PointSchema


def create_summary(points: Dict[Point, PointSchema]) -> SummarySchema:
    """
    Creates a summary of the calculated points.

    - Finds the sign of the sun, moon, and ascendant.
    - Finds the planet that rules the ascendant.
    - Determines whether the chart is during the day.

    :param points: The current collection of calculated points.

    :return: The calculated chart summary.
    """

    # Return an empty summary if the big 3 points are not all calculated
    if Point.sun not in points or Point.moon not in points or Point.ascendant not in points:
        return SummarySchema()

    sun, moon, asc = points[Point.sun], points[Point.moon], points[Point.ascendant]

    return SummarySchema(
        sun=sun.sign, moon=moon.sign, asc=asc.sign,
        asc_ruler=zodiac_sign_traits.signs[asc.sign].rulership,
        is_day_time=calculate_is_day_time(sun.degrees_from_aries, asc.degrees_from_aries)
    )


def calculate_is_day_time(sun_degrees_from_aries, asc_degrees_from_aries) -> bool:
    """
    Returns whether the current points are during the day by looking if the sun is below the horizon.

    :param sun_degrees_from_aries: The degrees from aries of the sun.
    :param asc_degrees_from_aries: The degrees from aries of the ascendant, representing the horizon.

    :return: Whether these points are found at day time.
    """

    positive_difference_in_degrees = (sun_degrees_from_aries - asc_degrees_from_aries) % 360

    return positive_difference_in_degrees > 180
