from astro.schema import PointSchema
from astro.util import ZodiacSign, zodiac_sign_order
from astro.collection.point_traits import point_traits


def calculate_point_attributes(point: PointSchema, stationary_pct_of_avg_speed: float = 0.3):
    """
    Calculates all derived attributes for a point.

    - Sets the properties `sign`, `degrees_in_sign`, `minutes_in_degree`, `is_stationary`,
      and `is_retrograde` within the point object.

    :param point: The point to calculate attributes for.
    :param stationary_pct_of_avg_speed: The percent of the average speed of the point
     that a point must be under to be considered stationary.
    """

    point.sign = calculate_sign(point.degrees_from_aries)
    point.degrees_in_sign = calculate_degrees_in_sign(point.degrees_from_aries)
    point.minutes_in_degree = calculate_minutes_in_degree(point.degrees_from_aries)

    calculate_speed_properties(point, stationary_pct_of_avg_speed)


def calculate_sign(degrees_from_aries: float) -> ZodiacSign:
    """
    Calculates what zodiac sign a point falls within.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's zodiac sign.
    """

    twelfth_of_circle = int(degrees_from_aries / 30)

    return zodiac_sign_order[twelfth_of_circle]


def calculate_degrees_in_sign(degrees_from_aries: float) -> int:
    """
    Calculates how many degrees this point is at within its zodiac sign.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's integer degrees within its zodiac sign, out of 30.
    """

    return int(degrees_from_aries % 30)


def calculate_minutes_in_degree(degrees_from_aries: float) -> int:
    """
    Calculates how many minutes this point is at within the current degree.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's integer minutes of the current degree, out of 60.
    """

    fraction_of_degree = degrees_from_aries % 1
    degrees_per_minute = 60

    return int(fraction_of_degree * degrees_per_minute)


def calculate_speed_properties(point: PointSchema, stationary_pct_of_avg_speed: float = 0.3):
    """
    Calculates whether a point is retrograde or stationing based on its speed.

    - Only calculates speed properties when the point in time has a speed and the point has a known
      average speed.

    - Sets the properties `is_stationary` and `is_retrograde` within the point object.

    - Uses the speed averages and the 30% of average speed for stationing found here:
      https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    :param point: The point to calculate speed attributes for.
    :param stationary_pct_of_avg_speed: The percent of the average speed of the point
     that a point must be under to be considered stationary.
    """

    if point.speed:
        point.is_retrograde = point.speed < 0

        if point.name in point_traits.points and point_traits.points[point.name].speed_avg:
            average_speed = point_traits.points[point.name].speed_avg
            threshold_speed = average_speed * stationary_pct_of_avg_speed

            point.is_stationary = 0 < point.speed < threshold_speed or 0 > point.speed > -threshold_speed
            point.is_retrograde = point.speed < 0
