from typing import Tuple, Dict

from .ephemeris import get_point_properties, get_angles
from astro.schema import EventSchema, PointSchema, EventSettingsSchema
from astro.util import Point
from .lot_factory import create_lot
from .midpoint_factory import create_midpoint
from .is_day_time import calculate_is_day_time
from ...collection import point_traits
from ...collection.lot_traits import lot_traits


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

    enabled_points = event_settings.get_all_enabled_points()
    enabled_midpoints = event_settings.get_all_enabled_midpoints()

    # Add the points for the angles.
    for point_in_time in create_angles(event_settings.event):
        if point_in_time.name in enabled_points:
            points[point_in_time.name] = point_in_time

    # Add each of the points with swiss ephemeris data.
    for point in point_traits.points:
        if point in enabled_points:
            points[point] = create_swe_point(event_settings.event, point)

    # Add the south node by reflecting the north node.
    if Point.north_mode in enabled_points and Point.south_node in enabled_points:
        points[Point.south_node] = create_south_node(points[Point.north_mode])

    # Add each midpoint that is enabled.
    for midpoint in enabled_midpoints:
        point = create_midpoint(points, midpoint)

        if point:
            points[str(midpoint)] = point

    is_day_time = calculate_is_day_time(points)

    # Add all lots.
    for lot in lot_traits.lots:
        if lot in enabled_points:
            point = create_lot(points, lot, is_day_time)

            if point:
                points[lot] = point

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
            points=[Point.ascendant],
            longitude=asc[0],
            longitude_velocity=asc[1],
            declination=asc[2],
        ),
        PointSchema(
            name=Point.midheaven,
            points=[Point.midheaven],
            longitude=mc[0],
            longitude_velocity=mc[1],
            declination=mc[2],
        ),
        PointSchema(
            name=Point.descendant,
            points=[Point.descendant],
            longitude=desc[0],
            longitude_velocity=desc[1],
            declination=desc[2],
        ),
        PointSchema(
            name=Point.inner_heaven,
            points=[Point.inner_heaven],
            longitude=ic[0],
            longitude_velocity=ic[1],
            declination=ic[2],
        ),
        PointSchema(
            name=Point.vertex,
            points=[Point.vertex],
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
        points=[traits.name],
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
        points=[Point.south_node],
        longitude=longitude,
        longitude_velocity=north_node.longitude_velocity,
        declination=declination,
        declination_velocity=declination_velocity,
    )
