from typing import Tuple, Dict

from astro.util import ZodiacSign, Point, pointTraits, zodiacSignOrder, STATIONARY_PERCENT_OF_AVG_SPEED
from astro.schema import DateTimeLocation, PointInTime
from .ephemeris import get_julian_day, get_degrees_from_aries, get_declination, get_asc_mc, get_speed


def create_all_points(datetime: DateTimeLocation) -> Dict[Point, PointInTime]:
    """
    Creates a list of all calculated points.

    :param datetime: The current time and location.

    :return: The calculated points.
    """

    # Add the ascendant and midheaven.
    asc, mc = create_as_mc(datetime)

    points = {
        Point.ascendant: asc,
        Point.midheaven: mc
    }

    # Add each of the points with traits.
    for point in pointTraits.points:
        points[point] = create_point(datetime, point)

    points[Point.south_node] = create_south_node(points[Point.north_mode])

    # Calculate the derived point attributes for each point.
    for point in points.values():
        calculate_point_attributes(point)

    return points


def create_as_mc(datetime: DateTimeLocation) -> Tuple[PointInTime, PointInTime]:
    """
    Creates the points for the Ascendant and Midheaven

    :param datetime: The current time and location.

    :return: The ascendant and midheaven points.
    """

    day = get_julian_day(datetime.date)
    ascendant, midheaven = get_asc_mc(day, datetime.latitude, datetime.longitude)

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

    return PointInTime(
        name=Point.south_node,
        degrees_from_aries=round(south_node_degrees_from_aries, 2),
        declination=-north_node.declination,
        speed=north_node.speed
    )


def create_point(datetime: DateTimeLocation, point: Point) -> PointInTime:
    """
    Creates a point object for he given planet on the given day.

    :param datetime: The current time and location.
    :param point: The point to find.

    :return: The calculated point.
    """

    traits = pointTraits.points[point]
    day = get_julian_day(datetime.date)
    degrees_from_aries = get_degrees_from_aries(day, traits.swe_id)
    declination = get_declination(day, traits.swe_id)
    speed = get_speed(day, traits.swe_id)

    point_in_time = PointInTime(
        name=traits.name,
        degrees_from_aries=round(degrees_from_aries, 2),
        declination=round(declination, 2),
        speed=speed,
    )

    return point_in_time


def calculate_point_attributes(point: PointInTime):
    """
    Calculates all derived attributes for a point.

    :param point: The point to calculate attributes for.
    """

    point.sign = calculate_sign(point.degrees_from_aries)
    point.degrees_in_sign = calculate_degrees_in_sign(point.degrees_from_aries)
    point.minutes_in_degree = calculate_minutes_in_degree(point.degrees_from_aries)

    calculate_speed_properties(point)


def calculate_sign(degrees_from_aries: float) -> ZodiacSign:
    """
    Calculates what sign a point falls within.

    :param degrees_from_aries: The degrees this point is at relative to 0 degrees aries.

    :return: The point's zodiac sign.
    """

    twelfth_of_circle = int(degrees_from_aries / 30)

    return zodiacSignOrder[twelfth_of_circle]


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


def calculate_speed_properties(point: PointInTime):
    """
    Calculates whether the planet is retrograde and stationing.

    Uses the speed averages and the 30% of average speed for stationing found here:
    https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    :param point: The point to calculate speed attributes for.
    """

    if point.speed:
        point.is_retrograde = point.speed < 0

        if point.name in pointTraits.points and pointTraits.points[point.name].speed_avg:
            average_speed = pointTraits.points[point.name].speed_avg
            threshold_speed = average_speed * STATIONARY_PERCENT_OF_AVG_SPEED

            point.is_stationary = 0 < point.speed < threshold_speed or 0 > point.speed > -threshold_speed
            point.is_retrograde = point.speed < 0
