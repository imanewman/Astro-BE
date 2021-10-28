from typing import Tuple, Optional

from astro.schema import RelationshipSchema, PointSchema
from astro.util import EventType, AspectMovementType, AspectType


def calculate_degree_types(
        relationship: RelationshipSchema,
        from_item: Tuple[PointSchema, EventType],
        to_item: Tuple[PointSchema, EventType],
):
    """
    Calculates whether degree or declination aspects are applying or separating.

    - Sets the `relationship`'s attributes `degree_aspect_movement` and `declination_aspect_movement`
      to the direction of movement between the two points.

    :param relationship: The relationship between points to store calculations in.
    :param from_item: The starting point in the relationship, and the type of chart it is from.
    :param to_item: The ending point in the relationship, and the type of chart it is from.
    """

    relationship.degree_aspect_movement, relationship.degree_aspect_approx_days = \
        calculate_degree_types_from_speed(
            (from_item[0].longitude_velocity, from_item[1]),
            (to_item[0].longitude_velocity, to_item[1]),
            relationship.degree_aspect_orb
        )

    to_velocity = to_item[0].declination_velocity
    aspect_orb = relationship.declination_aspect_orb

    if relationship.declination_aspect == AspectType.contraparallel \
            and to_velocity is not None and aspect_orb is not None:
        to_velocity *= -1
        aspect_orb *= -1

    relationship.declination_aspect_movement, relationship.declination_aspect_approx_days = \
        calculate_degree_types_from_speed(
            (from_item[0].declination_velocity, from_item[1]),
            (to_velocity, to_item[1]),
            aspect_orb
        )


def calculate_degree_types_from_speed(
        from_item: Tuple[Optional[float], EventType],
        to_item: Tuple[Optional[float], EventType],
        orb: float
) -> Tuple[Optional[AspectMovementType], Optional[float]]:
    """
    Calculates whether points are applying or separating.

    :param from_item: The starting speed in the relationship, and the type of chart it is from.
    :param to_item: The ending speed in the relationship, and the type of chart it is from.
    :param orb: The orb between the two points.

    :return:
        [0] The direction of movement between the two speeds.
        [1] The approximate days until exact aspect.
    """

    if orb is None or from_item[0] is None or to_item[0] is None:
        return None, None

    from_velocity, to_velocity, is_same_direction = calculate_degree_types_direction(from_item, to_item)
    from_is_faster = from_velocity >= to_velocity
    relative_velocity = from_velocity - to_velocity
    approximate_days_until_exact = orb / relative_velocity

    if orb >= 0 if from_is_faster else orb < 0:
        # If the orb is positive and first object is faster,
        # or the orb is negative and the second object is faster,
        # the aspect is applying.
        degree_type = AspectMovementType.applying if is_same_direction \
            else AspectMovementType.mutually_applying

        return degree_type, approximate_days_until_exact
    if orb >= 0 if not from_is_faster else orb < 0:
        # If the orb is positive and second object is faster,
        # or the orb is negative and the first object is faster,
        # the aspect is separating.
        degree_type = AspectMovementType.separating if is_same_direction \
            else AspectMovementType.mutually_separating

        return degree_type, approximate_days_until_exact

    return None, None


def calculate_degree_types_direction(
        from_item: Tuple[float, EventType],
        to_item: Tuple[float, EventType]
) -> Tuple[float, float, bool]:
    """
    Calculates whether points are moving in the direction.

    :param from_item: The starting speed in the relationship, and the type of chart it is from.
    :param to_item: The ending speed in the relationship, and the type of chart it is from.

    :return: The from speed, the to speed, and whether the points are moving in the same direction.
    """

    from_velocity, from_event_type = from_item
    to_velocity, to_event_type = to_item

    # If aspects are between a transit chart and a base chart,
    # set the base speed to 0 and assert that the bodies are moving in the same direction.
    if from_event_type == EventType.transit and to_event_type != EventType.transit:
        return from_velocity, 0, True
    elif to_event_type == EventType.transit and from_event_type != EventType.transit:
        return 0, to_velocity, True

    return from_velocity, to_velocity, (from_velocity > 0) == (to_velocity > 0)
