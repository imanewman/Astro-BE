from typing import Tuple, Optional

from astro.schema import RelationshipSchema, PointSchema
from astro.util import EventType, AspectMovementType


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

    relationship.degree_aspect_movement = calculate_degree_types_longitude(
        (from_item[0].speed, from_item[1]),
        (to_item[0].speed, to_item[1]),
        relationship.degree_aspect_orb
    )

    # TODO
    # relationship.declination_aspect_movement = calculate_degree_types_from_speed(
    #     (from_item[0].declination_speed, from_item[1]),
    #     (to_item[0].declination_speed, to_item[1]),
    #     relationship.declination_aspect_orb,
    #     relationship.declination_aspect
    # )


def calculate_degree_types_longitude(
        from_item: Tuple[Optional[float], EventType],
        to_item: Tuple[Optional[float], EventType],
        orb: float
) -> Optional[AspectMovementType]:
    """
    Calculates whether points are applying or separating.

    :param from_item: The starting speed in the relationship, and the type of chart it is from.
    :param to_item: The ending speed in the relationship, and the type of chart it is from.
    :param orb: The orb between the two points.

    :return: The direction of movement between the two speeds.
    """

    if orb is None or from_item[0] is None or to_item[0] is None:
        return

    from_speed, to_speed, is_same_direction = calculate_degree_types_direction(from_item, to_item)

    if (orb >= 0 and from_speed >= to_speed) or (orb < 0 and from_speed < to_speed):
        # If the orb is positive and first object is faster,
        # or the orb is negative and the second object is faster,
        # the aspect is applying.
        return AspectMovementType.applying if is_same_direction \
            else AspectMovementType.mutually_applying
    if (orb >= 0 and from_speed < to_speed) or (orb < 0 and from_speed >= to_speed):
        # If the orb is positive and second object is faster,
        # or the orb is negative and the first object is faster,
        # the aspect is separating.
        return AspectMovementType.separating if is_same_direction \
            else AspectMovementType.mutually_separating


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

    from_speed, from_event_type = from_item
    to_speed, to_event_type = to_item

    # If aspects are between a transit chart and a base chart,
    # set the base speed to 0 and assert that the bodies are moving in the same direction.
    if from_event_type == EventType.transit and to_event_type != EventType.transit:
        return from_speed, 0, True
    elif to_event_type == EventType.transit and from_event_type != EventType.transit:
        return 0, to_speed, True

    return from_speed, to_speed, (from_speed > 0) == (to_speed > 0)
