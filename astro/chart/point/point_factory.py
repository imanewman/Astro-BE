from typing import Tuple, Dict

from .ephemeris import get_point_properties, get_angles
from astro.schema import EventSchema, PointSchema, EventSettingsSchema, MidpointSettingsSchema
from astro.util import Point
from ...collection import point_traits


def create_points(
        event_settings: EventSettingsSchema,
) -> Dict[Point, PointSchema]:
    """
    Creates a list of all calculated points.

    - Assumes the julian day has been calculated and set on the event.

    :param event_settings: The current time, location, and enabled points.

    :return: The calculated points.
    """
    points = {}

    # Add the points for the angles.
    for point_in_time in create_angles(event_settings.event):
        if point_in_time.name in event_settings.enabled_points:
            points[point_in_time.name] = point_in_time

    # Add each of the points with swiss ephemeris data.
    for point in point_traits.points:
        if point in event_settings.enabled_points:
            points[point] = create_swe_point(event_settings.event, point)

    # Add the south node by reflecting the north node.
    if Point.north_mode in event_settings.enabled_points:
        points[Point.south_node] = create_south_node(points[Point.north_mode])

    # Add each midpoint that is enabled.
    for midpoint in event_settings.enabled_midpoints:
        points[str(midpoint)] = create_midpoint(points, midpoint)

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

    return PointSchema(
        name=traits.name,
        longitude=longitude,
        longitude_velocity=longitude_velocity,
        declination=declination,
        declination_velocity=declination_velocity,
    )


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


def create_midpoint(points: Dict[Point, PointSchema], midpoint: MidpointSettingsSchema) -> PointSchema:
    """
    Creates a midpoint from the existing points.

    :param points: A collection of already created points.
    :param midpoint: The midpoint to create.

    :return: The calculated midpoint object with calculated degrees from aries, declination, and speed.
    """
    if midpoint.from_point not in points:
        raise Exception(f"Unable to create midpoint: {midpoint.from_point} has not been calculated")
    elif midpoint.to_point not in points:
        raise Exception(f"Unable to create midpoint: {midpoint.to_point} has not been calculated")

    from_point_in_time = points[midpoint.from_point]
    to_point_in_time = points[midpoint.to_point]

    midpoint_longitude = \
        ((to_point_in_time.longitude - from_point_in_time.longitude) / 2 + from_point_in_time.longitude) % 360
    midpoint_declination = \
        (to_point_in_time.declination - from_point_in_time.declination) / 2 + from_point_in_time.declination

    opposite_midpoint_longitude = (midpoint_longitude + 180) % 360
    distance_to_midpoint = to_point_in_time.longitude - midpoint_longitude % 360
    opposite_distance_to_midpoint = to_point_in_time.longitude - opposite_midpoint_longitude % 360

    if opposite_distance_to_midpoint < distance_to_midpoint:
        # Ensure that the closer midpoint is the one used.
        midpoint_longitude = opposite_midpoint_longitude

    midpoint_longitude_velocity = 0
    midpoint_declination_velocity = 0

    return PointSchema(
        name=str(midpoint),
        longitude=midpoint_longitude,
        longitude_velocity=midpoint_longitude_velocity,
        declination=midpoint_declination,
        declination_velocity=midpoint_declination_velocity,
    )
