from typing import Dict, Optional

from astro.schema import PointSchema, MidpointSettingsSchema
from astro.util import Point


def create_midpoint(
        points: Dict[Point, PointSchema],
        midpoint: MidpointSettingsSchema
) -> Optional[PointSchema]:
    """
    Creates a midpoint from the existing points.

    :param points: A collection of already created points.
    :param midpoint: The midpoint to create.

    :return: The calculated midpoint object with calculated degrees from aries, declination, and speed.
    """
    if midpoint.from_point not in points or midpoint.to_point not in points:
        return

    from_point = points[midpoint.from_point]
    to_point = points[midpoint.to_point]

    return PointSchema(
        name=str(midpoint),
        points=[midpoint.from_point, midpoint.to_point],
        longitude=calculate_midpoint_longitude(from_point, to_point),
        longitude_velocity=calculate_average_longitude_velocity(from_point, to_point),
        declination=calculate_midpoint_declination(from_point, to_point),
        declination_velocity=calculate_average_declination_velocity(from_point, to_point),
    )


def calculate_midpoint_longitude(
    from_point: PointSchema,
    to_point: PointSchema,
) -> float:
    """
    Calculates the longitude of the midpoint between points.

    :param from_point: The first point of the midpoint.
    :param to_point: The second point of the midpoint.

    :return: The midpoint longitude.
    """
    midpoint_longitude = (to_point.longitude + from_point.longitude) / 2
    distance_to_midpoint = abs(to_point.longitude - midpoint_longitude)

    # Ensure that the closer midpoint is the one used.
    if distance_to_midpoint > 90:
        return (midpoint_longitude + 180) % 360
    else:
        return midpoint_longitude


def calculate_average_longitude_velocity(
    from_point: PointSchema,
    to_point: PointSchema,
) -> Optional[float]:
    """
    Calculates the average velocity between points.

    :param from_point: The first point of the midpoint.
    :param to_point: The second point of the midpoint.

    :return: The average velocity.
    """
    if from_point.longitude_velocity is not None \
            and to_point.longitude_velocity is not None:
        return (to_point.longitude_velocity + from_point.longitude_velocity) / 2


def calculate_midpoint_declination(
    from_point: PointSchema,
    to_point: PointSchema,
) -> Optional[float]:
    """
    Calculates the declination midpoint between points.

    :param from_point: The first point of the midpoint.
    :param to_point: The second point of the midpoint.

    :return: The midpoint declination.
    """
    if from_point.declination is not None and to_point.declination is not None:
        return (to_point.declination + from_point.declination) / 2


def calculate_average_declination_velocity(
    from_point: PointSchema,
    to_point: PointSchema,
) -> Optional[float]:
    """
    Calculates the average declination velocity between points.

    :param from_point: The first point of the midpoint.
    :param to_point: The second point of the midpoint.

    :return: The average declination velocity.
    """
    if from_point.declination_velocity is not None \
            and to_point.declination_velocity is not None:
        return (to_point.declination_velocity + from_point.declination_velocity) / 2
