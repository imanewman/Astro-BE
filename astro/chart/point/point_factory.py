from typing import Tuple, Dict, List

from .ephemeris import get_point_properties, get_angles
from astro.schema import EventSchema, PointSchema
from astro.util import Point, default_enabled_points
from ...collection import point_traits


def create_points(
        event: EventSchema,
        enabled_points: List[Point] = default_enabled_points
) -> Dict[Point, PointSchema]:
    """
    Creates a list of all calculated points.

    - Assumes the julian day has been calculated and set on the event.

    :param event: The current time and location.
    :param enabled_points: The points that should be created.

    :return: The calculated points.
    """
    points = {}

    # Add the points for the angles.
    for point_in_time in create_angles(event):
        if point_in_time.name in enabled_points:
            points[point_in_time.name] = point_in_time

    # Add each of the points with swiss ephemeris data.
    for point in point_traits.points:
        if point in enabled_points:
            points[point] = create_swe_point(event, point)

    # Add the south node by reflecting the north node.
    if Point.north_mode in enabled_points:
        points[Point.south_node] = create_south_node(points[Point.north_mode])

    return points


def create_angles(event: EventSchema) -> Tuple[PointSchema, PointSchema, PointSchema, PointSchema, PointSchema]:
    """
    Creates points for the Ascendant, MC, Descendant, IC, and Vertex at the given time and location.

    - Assumes the julian day has been calculated and set on the event.

    :param event: The current date, time, and location.

    :return:
        [0] The Ascendant point for the given event.
        [1] The Midheaven point for the given event.
        [2] The Descendant point for the given event.
        [3] The IC point for the given event.
        [4] The Vertex point for the given event.
    """
    asc, mc, desc, ic, vertex = get_angles(event.julian_day, event.latitude, event.longitude)

    return (
        PointSchema(
            name=Point.ascendant,
            longitude=asc[0],
            longitude_velocity=asc[1],
            declination=asc[2],
        ),
        PointSchema(
            name=Point.midheaven,
            longitude=mc[0],
            longitude_velocity=mc[1],
            declination=mc[2],
        ),
        PointSchema(
            name=Point.descendant,
            longitude=desc[0],
            longitude_velocity=desc[1],
            declination=desc[2],
        ),
        PointSchema(
            name=Point.inner_heaven,
            longitude=ic[0],
            longitude_velocity=ic[1],
            declination=ic[2],
        ),
        PointSchema(
            name=Point.vertex,
            longitude=vertex[0],
            longitude_velocity=vertex[1],
            declination=vertex[2],
        )
    )


def create_swe_point(event: EventSchema, point: Point) -> PointSchema:
    """
    Creates a point object for a point name at the given time and location.

    - Assumes the julian day has been calculated and set on the event.

    :param event: The current time and location.
    :param point: The name of the point to create.

    :return: The calculated point object with calculated degrees from aries, declination, and speed.
    """
    if point not in point_traits.points:
        raise Exception(f"No point traits exist for: {point}")

    traits = point_traits.points[point]
    longitude, longitude_velocity, declination, declination_velocity = \
        get_point_properties(event.julian_day, traits.swe_id)

    point_in_time = PointSchema(
        name=traits.name,
        longitude=longitude,
        longitude_velocity=longitude_velocity,
        declination=declination,
        declination_velocity=declination_velocity,
    )

    return point_in_time


def create_south_node(north_node: PointSchema) -> PointSchema:
    """
    Creates the south node by reflecting the degrees from aries and declination of the north node.

    :param north_node: The current location of the north node.

    :return: The current location of the south node.
    """
    longitude = (north_node.longitude + 180) % 360
    declination = north_node.declination and -north_node.declination
    declination_velocity = north_node.declination_velocity and -north_node.declination_velocity

    return PointSchema(
        name=Point.south_node,
        longitude=longitude,
        longitude_velocity=north_node.longitude_velocity,
        declination=declination,
        declination_velocity=declination_velocity,
    )