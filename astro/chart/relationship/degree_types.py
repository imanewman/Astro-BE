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

    relationship.degree_aspect_movement = calculate_degree_types_from_speed(
        (from_item[0].speed, from_item[1]),
        (to_item[0].speed, to_item[1]),
        relationship.degree_aspect_orb
    )

    relationship.declination_aspect_movement = calculate_degree_types_from_speed(
        (from_item[0].declination_speed, from_item[1]),
        (to_item[0].declination_speed, to_item[1]),
        relationship.declination_aspect_orb,
        relationship.declination_aspect
    )


def calculate_degree_types_from_speed(
        from_item: Tuple[float, EventType],
        to_item: Tuple[float, EventType],
        orb: float,
        declination_aspect: Optional[AspectType] = None
) -> Optional[AspectMovementType]:
    """
    Calculates whether aspects are applying or separating.

    :param from_item: The starting speed in the relationship, and the type of chart it is from.
    :param to_item: The ending speed in the relationship, and the type of chart it is from.
    :param orb: The orb between the two points.
    :param declination_aspect: The type of declination aspect, if one exists.

    :return: The direction of movement between the two speeds.
    """
    from_speed, from_event_type = from_item
    to_speed, to_event_type = to_item

    if orb is not None and from_speed is not None and to_speed is not None:
        # TODO: handle contraparallels properly
        # if declination_aspect == AspectType.contraparallel:
        #     # For contraparallel aspects, reflect the speed.
        #     to_speed = abs(to_speed)
        #     from_speed = abs(to_speed)

        moving_in_same_direction = (from_speed > 0) == (to_speed > 0)

        # If aspects are between a transit chart and a base chart,
        # set the base speed to 0 and assert that the bodies are moving in the same direction.
        if from_event_type == EventType.transit and to_event_type != EventType.transit:
            to_speed = 0
            moving_in_same_direction = True
        elif to_event_type == EventType.transit and from_event_type != EventType.transit:
            from_speed = 0
            moving_in_same_direction = True

        if (orb >= 0 and from_speed >= to_speed) or (orb < 0 and from_speed < to_speed):
            # If the orb is positive and first object is faster,
            # or the orb is negative and the second object is faster,
            # the aspect is applying.
            return AspectMovementType.applying if moving_in_same_direction \
                else AspectMovementType.mutually_applying
        if (orb >= 0 and from_speed < to_speed) or (orb < 0 and from_speed >= to_speed):
            # If the orb is positive and second object is faster,
            # or the orb is negative and the first object is faster,
            # the aspect is separating.
            return AspectMovementType.separating if moving_in_same_direction \
                else AspectMovementType.mutually_separating
