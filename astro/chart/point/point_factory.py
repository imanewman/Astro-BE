from typing import Tuple, Dict

from .ephemeris import get_asc_mc, get_point_properties
from astro.schema import EventSchema, PointInTime
from astro.util import Point, point_traits


def create_points(event: EventSchema) -> Dict[Point, PointInTime]:
    """
    Creates a list of all calculated points.

    Assumptions
    ----------
    - Assumes the julian day has been calculated and set on the event.

    :param event: The current time and location.

    :return: The calculated points.
    """

    points = {}

    # Add the ascendant and midheaven.
    for point_in_time in create_asc_mc(event):
        points[point_in_time.name] = point_in_time

    # Add each of the points with swiss ephemeris data.
    for point in point_traits.points:
        points[point] = create_swe_point(event, point)

    # Add the south node by reflecting the north node.
    points[Point.south_node] = create_south_node(points[Point.north_mode])

    return points


def create_asc_mc(event: EventSchema) -> Tuple[PointInTime, PointInTime]:
    """
    Creates points for the ascendant and midheaven at the given time and location.

    Assumptions
    ----------
    - Assumes the julian day has been calculated and set on the event.

    :param event: The current date, time, and location.

    :return:
        [0] The ascendant point for the given event.
        [1] The midheaven point for the given event.
    """

    ascendant, midheaven = get_asc_mc(event.julian_day, event.latitude, event.longitude)

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


def create_swe_point(event: EventSchema, point: Point) -> PointInTime:
    """
    Creates a point object for a point name at the given time and location.

    Assumptions
    ----------
    - Assumes the julian day has been calculated and set on the event.

    :param event: The current time and location.
    :param point: The name of the point to create.

    :return: The calculated point object with calculated degrees from aries, declination, and speed.
    """

    if point not in point_traits.points:
        raise Exception(f"No point traits exist for: {point}")

    traits = point_traits.points[point]
    degrees_from_aries, declination, speed = get_point_properties(event.julian_day, traits.swe_id)

    point_in_time = PointInTime(
        name=traits.name,
        degrees_from_aries=round(degrees_from_aries, 2),
        declination=round(declination, 2),
        speed=round(speed, 4),
    )

    return point_in_time


def create_south_node(north_node: PointInTime) -> PointInTime:
    """
    Creates the south node by reflecting the degrees from aries and declination of the north node.

    :param north_node: The current location of the north node.

    :return: The current location of the south node.
    """

    south_node_degrees_from_aries = round((north_node.degrees_from_aries + 180) % 360, 2)
    declination = north_node.declination and -north_node.declination

    return PointInTime(
        name=Point.south_node,
        degrees_from_aries=south_node_degrees_from_aries,
        declination=declination,
        speed=north_node.speed
    )