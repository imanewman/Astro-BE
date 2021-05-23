from typing import Tuple, Dict

from astro.util import ZodiacSign, Point, point_traits, zodiac_sign_order
from astro.schema import DateTimeLocation, PointInTime
from .ephemeris import get_julian_day, get_degrees_from_aries, get_declination, get_asc_mc, get_speed


def create_all_points(datetime: DateTimeLocation, stationary_pct_of_avg_speed: float = 0.3) -> Dict[Point, PointInTime]:
    """
    Creates a list of all calculated points.

    :param datetime: The current time and location.

    :return: The calculated points.
    :param stationary_pct_of_avg_speed: The percent of the average planet speed needed to be considered stationary.
    """

    # Set the julian day for the time
    datetime.julian_day = get_julian_day(datetime.date)

    # Add the ascendant and midheaven.
    asc, mc = create_asc_mc(datetime)

    points = {
        Point.ascendant: asc,
        Point.midheaven: mc
    }

    # Add each of the points with traits.
    for point in point_traits.points:
        points[point] = create_point(datetime, point)

    points[Point.south_node] = create_south_node(points[Point.north_mode])

    # Calculate the derived point attributes for each point.
    for point in points.values():
        calculate_point_attributes(point, stationary_pct_of_avg_speed)

    return points


def create_asc_mc(datetime: DateTimeLocation) -> Tuple[PointInTime, PointInTime]:
    """
    Creates the points for the Ascendant and Midheaven.

    :param datetime: The current time and location. Assumes the julian day has been calculated.

    :return: The ascendant and midheaven points.
    """

    ascendant, midheaven = get_asc_mc(datetime.julian_day, datetime.latitude, datetime.longitude)

    return (
        PointInTime(
            name=Point.ascendant,
            degrees_from_aries=round(ascendant, 2),
        ),
        PointInTime(
            name=Point.midheaven,
            degrees_from_aries=round(midheaven, 2),
        )
    )


def create_south_node(north_node: PointInTime) -> PointInTime:
    """
    Creates the south node directly opposite from the north node.

    :param north_node: The current location of the north node.

    :return: The current location of the south node.
    """

    south_node_degrees_from_aries = (north_node.degrees_from_aries + 180) % 360
    declination = -north_node.declination if north_node.declination else None

    return PointInTime(
        name=Point.south_node,
        degrees_from_aries=round(south_node_degrees_from_aries, 2),
        declination=declination,
        speed=north_node.speed
    )


def create_point(datetime: DateTimeLocation, point: Point) -> PointInTime:
    """
    Creates a point object for the given planet on the given day.

    :param datetime: The current time and location. Assumes the julian day has been calculated.
    :param point: The point to find.

    :return: The calculated point.
    """

    traits = point_traits.points[point]
    degrees_from_aries = get_degrees_from_aries(datetime.julian_day, traits.swe_id)
    declination = get_declination(datetime.julian_day, traits.swe_id)
    speed = get_speed(datetime.julian_day, traits.swe_id)

    point_in_time = PointInTime(
        name=traits.name,
        degrees_from_aries=round(degrees_from_aries, 2),
        declination=round(declination, 2),
        speed=speed,
    )

    return point_in_time


def calculate_point_attributes(point: PointInTime, stationary_pct_of_avg_speed: float = 0.3):
    """
    Calculates all derived attributes for a point.

    :param point: The point to calculate attributes for.
    :param stationary_pct_of_avg_speed: The percent of the average planet speed needed to be considered stationary.
    """

    point.sign = calculate_sign(point.degrees_from_aries)
    point.degrees_in_sign = calculate_degrees_in_sign(point.degrees_from_aries)
    point.minutes_in_degree = calculate_minutes_in_degree(point.degrees_from_aries)

    calculate_speed_properties(point, stationary_pct_of_avg_speed)


def calculate_sign(degrees_from_aries: float) -> ZodiacSign:
    """
    Calculates what sign a point falls within.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's zodiac sign.
    """

    twelfth_of_circle = int(degrees_from_aries / 30)

    return zodiac_sign_order[twelfth_of_circle]


def calculate_degrees_in_sign(degrees_from_aries: float) -> int:
    """
    Calculates how many degrees this point is at within its current sign.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's zodiac sign degrees, out of 30.
    """

    return int(degrees_from_aries % 30)


def calculate_minutes_in_degree(degrees_from_aries: float) -> int:
    """
    Calculates how many minutes this point is at of the current degree.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's minutes of the current degree, out of 60.
    """

    fraction_of_degree = degrees_from_aries % 1
    degrees_per_minute = 60

    return int(fraction_of_degree * degrees_per_minute)


def calculate_speed_properties(point: PointInTime, stationary_pct_of_avg_speed: float = 0.3):
    """
    Calculates whether the planet is retrograde and stationing.

    Uses the speed averages and the 30% of average speed for stationing found here:
    https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    :param point: The point to calculate speed attributes for.
    :param stationary_pct_of_avg_speed: The percent of the average planet speed needed to be considered stationary.
    """

    if point.speed:
        point.is_retrograde = point.speed < 0

        if point.name in point_traits.points and point_traits.points[point.name].speed_avg:
            average_speed = point_traits.points[point.name].speed_avg
            threshold_speed = average_speed * stationary_pct_of_avg_speed

            point.is_stationary = 0 < point.speed < threshold_speed or 0 > point.speed > -threshold_speed
            point.is_retrograde = point.speed < 0
