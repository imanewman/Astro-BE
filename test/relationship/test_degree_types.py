from typing import Tuple, Optional

from astro.chart import calculate_degree_types
from astro.schema import RelationshipSchema
from astro.util import EventType
from test.utils import create_test_points


def create_longitude_separated_points(
        degrees_of_separation: int,
        from_item: Tuple[Optional[float], EventType],
        to_item: Tuple[Optional[float], EventType],
) -> RelationshipSchema:
    """
    Creates a relationship and calculates whether aspects are applying or separating.

    :param degrees_of_separation: The degrees of separation between points.
    :param from_item: The starting longitude speed, declination speed, and the type of chart it is from.
    :param to_item: The ending longitude speed, declination speed, and the type of chart it is from.

    :return: The created relationship.
    """

    from_point, to_point = create_test_points(
        {
            "degrees_from_aries": 0,
            "speed": from_item[0],
        },
        {
            "degrees_from_aries": degrees_of_separation % 360,
            "speed": from_item[0],
        },
    )
    relationship = RelationshipSchema(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_types(
        relationship,
        (from_point, from_item[1]),
        (to_point, to_item[1])
    )

    return relationship


def test_calculate_degree_types__longitude__no_speed():
    """
    Tests calculating degree types when no speeds are given.
    """

    relationship = create_longitude_separated_points(
        5,
        (None, EventType.event),
        (None, EventType.event),
    )

    assert relationship.degree_aspect_movement is None
