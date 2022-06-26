from astro.collection import zodiac_sign_traits
from astro.schema import PointSchema, SettingsSchema
from astro.util import ZodiacSign, zodiac_sign_order
from astro.collection.point_traits import point_traits


def calculate_point_attributes(
        point: PointSchema,
        settings: SettingsSchema = SettingsSchema()
):
    """
    Calculates all derived attributes for a point.

    - Sets the properties `sign`, `degrees_in_sign`, `minutes_in_degree`, `is_stationary`,
      and `is_retrograde` within the point object.

    :param point: The point to calculate attributes for.
    :param settings: Settings used for calculations.
    """
    point.sign = calculate_sign(point.longitude)
    sign_traits = zodiac_sign_traits.signs[point.sign]
    point.modality = sign_traits.modality
    point.element = sign_traits.element

    point.degrees_in_sign = calculate_degrees_in_sign(point.longitude)
    point.minutes_in_degree = calculate_minutes_in_degree(point.longitude)

    calculate_velocity_properties(point, settings.stationary_pct_of_avg_speed)


def calculate_sign(longitude: float) -> ZodiacSign:
    """
    Calculates what zodiac sign a point falls within.

    :param longitude: The degrees this point is at relative to 0 degrees aries.

    :return: The point's zodiac sign.
    """
    twelfth_of_circle = int(longitude / 30)

    return zodiac_sign_order[twelfth_of_circle]


def calculate_degrees_in_sign(longitude: float) -> int:
    """
    Calculates how many degrees this point is at within its zodiac sign.

    :param longitude: The degrees this point is at relative to 0 degrees aries.

    :return: The point's integer degrees within its zodiac sign, out of 30.
    """
    return int(longitude % 30)


def calculate_minutes_in_degree(longitude: float) -> int:
    """
    Calculates how many minutes this point is at within the current degree.

    :param longitude: The degrees this point is at relative to 0 degrees aries.

    :return: The point's integer minutes of the current degree, out of 60.
    """
    fraction_of_degree = longitude % 1
    degrees_per_minute = 60

    return int(fraction_of_degree * degrees_per_minute)


def calculate_velocity_properties(point: PointSchema, stationary_pct_of_avg_speed: float = 0.3):
    """
    Calculates whether a point is retrograde or stationing based on its velocity.

    - Only calculates velocity properties when the point in time has a velocity and the point has a known
      average speed.

    - Sets the properties `is_stationary` and `is_retrograde` within the point object.

    - Uses the velocity averages and the 30% of average velocity for stationing found here:
      https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    :param point: The point to calculate velocity attributes for.
    :param stationary_pct_of_avg_speed: The percent of the average velocity of the point
                                        that a point must be under to be considered stationary.
    """
    if point.longitude_velocity is None:
        return

    point.is_retrograde = point.longitude_velocity < 0

    if point.name not in point_traits.points or not point_traits.points[point.name].speed_avg:
        return

    average_speed = point_traits.points[point.name].speed_avg
    threshold_speed = average_speed * stationary_pct_of_avg_speed

    point.is_stationary = -threshold_speed < point.longitude_velocity < threshold_speed
    point.is_retrograde = point.longitude_velocity < 0
