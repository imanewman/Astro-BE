from typing import Tuple, Optional

from astro.chart import calculate_degree_types, calculate_degree_aspect
from astro.chart.relationship.degree_types import calculate_degree_types_direction
from astro.schema import RelationshipSchema
from astro.util import EventType, AspectMovementType
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
            "speed": to_item[0],
        },
    )
    relationship = RelationshipSchema(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspect(relationship, from_point, to_point)

    calculate_degree_types(
        relationship,
        (from_point, from_item[1]),
        (to_point, to_item[1])
    )

    return relationship


def test_calculate_degree_types_direction__from_transit():
    """
    Tests calculating whether aspects are applying from an event to transit chart.
    Speeds for the transit chart are set to 0.
    """

    from_speed, to_speed, is_same_direction = calculate_degree_types_direction(
        (1, EventType.event),
        (1, EventType.transit),
    )

    assert from_speed == 0
    assert to_speed == 1
    assert is_same_direction is True


def test_calculate_degree_types_direction__to_transit():
    """
    Tests calculating whether aspects are applying from an event to transit chart.
    Speeds for the transit chart are set to 0.
    """

    from_speed, to_speed, is_same_direction = calculate_degree_types_direction(
        (1, EventType.transit),
        (1, EventType.event),
    )

    assert from_speed == 1
    assert to_speed == 0
    assert is_same_direction is True


def test_calculate_degree_types_direction__same_direction():
    """
    Tests calculating whether aspects are applying from an event to transit chart.
    Speeds for the transit chart are set to 0.
    """

    from_speed, to_speed, is_same_direction = calculate_degree_types_direction(
        (1, EventType.event),
        (1, EventType.event),
    )

    assert from_speed == 1
    assert to_speed == 1
    assert is_same_direction is True


def test_calculate_degree_types_direction__different_direction():
    """
    Tests calculating whether aspects are applying from an event to transit chart.
    Speeds for the transit chart are set to 0.
    """

    from_speed, to_speed, is_same_direction = calculate_degree_types_direction(
        (1, EventType.event),
        (-1, EventType.event),
    )

    assert from_speed == 1
    assert to_speed == -1
    assert is_same_direction is False


def test_calculate_degree_types_longitude__no_speed():
    """
    Tests calculating degree types when no speeds are given.
    """

    relationship = create_longitude_separated_points(
        1,
        (None, EventType.event),
        (None, EventType.event),
    )

    assert relationship.degree_aspect_movement is None


def test_calculate_degree_types_longitude__no_orb():
    """
    Tests calculating degree types with no orb of aspect between them.
    """

    relationship = create_longitude_separated_points(
        20,
        (1, EventType.event),
        (-1, EventType.event),
    )

    assert relationship.degree_aspect_movement is None


def test_calculate_degree_types_longitude__applying_positive():
    """
    Tests calculating degree types with a positive applying orb.
    """

    relationship = create_longitude_separated_points(
        1,
        (2, EventType.event),
        (1, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.applying


def test_calculate_degree_types_longitude__applying_negative():
    """
    Tests calculating degree types with a negative applying orb.
    """

    relationship = create_longitude_separated_points(
        -1,
        (1, EventType.event),
        (2, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.applying


def test_calculate_degree_types_longitude__mutually_applying_positive():
    """
    Tests calculating degree types with a positive mutually applying orb.
    """

    relationship = create_longitude_separated_points(
        1,
        (2, EventType.event),
        (-1, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.mutually_applying


def test_calculate_degree_types_longitude__mutually_applying_negative():
    """
    Tests calculating degree types with a negative mutually applying orb.
    """

    relationship = create_longitude_separated_points(
        -1,
        (-2, EventType.event),
        (1, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.mutually_applying


def test_calculate_degree_types_longitude__separating_positive():
    """
    Tests calculating degree types with a positive separating orb.
    """

    relationship = create_longitude_separated_points(
        1,
        (1, EventType.event),
        (2, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.separating


def test_calculate_degree_types_longitude__separating_negative():
    """
    Tests calculating degree types with a negative separating orb.
    """

    relationship = create_longitude_separated_points(
        -1,
        (2, EventType.event),
        (1, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.separating


def test_calculate_degree_types_longitude__mutually_separating_positive():
    """
    Tests calculating degree types with a positive mutually separating orb.
    """

    relationship = create_longitude_separated_points(
        1,
        (-1, EventType.event),
        (2, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.mutually_separating


def test_calculate_degree_types_longitude__mutually_separating_negative():
    """
    Tests calculating degree types with a negative mutually separating orb.
    """

    relationship = create_longitude_separated_points(
        -1,
        (2, EventType.event),
        (-1, EventType.event),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.mutually_separating


def test_calculate_degree_types_longitude__applying_transit():
    """
    Tests calculating degree types applying by transit.
    """

    relationship = create_longitude_separated_points(
        1,
        (-1, EventType.event),
        (-1, EventType.transit),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.applying


def test_calculate_degree_types_longitude__separating_transit():
    """
    Tests calculating degree types separating by transit.
    """

    relationship = create_longitude_separated_points(
        1,
        (-1, EventType.event),
        (1, EventType.transit),
    )

    assert relationship.degree_aspect_movement == AspectMovementType.separating
