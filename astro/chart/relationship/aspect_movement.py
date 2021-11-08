import datetime
from typing import Tuple, Optional

from astro.schema import RelationshipSchema, PointSchema, AspectSchema, EventSchema
from astro.util import EventType, AspectMovementType, AspectType


def calculate_aspect_movement(
        relationship: RelationshipSchema,
        from_item: Tuple[PointSchema, EventSchema],
        to_item: Tuple[PointSchema, EventSchema],
):
    """
    Calculates whether degree or declination aspects are applying or separating.

    - Sets each aspect's `movement` `days_until_exact`, `utc_date_of_exact`, and `local_date_of_exact`
      if there is an orb of aspect and both objects have a speed.

    :param relationship: The relationship between points to store calculations in.
    :param from_item: The starting point in the relationship, and the event it is from.
    :param to_item: The ending point in the relationship, and the event it is from.
    """

    calculate_aspect_movement_ecliptic(relationship, from_item, to_item)
    calculate_aspect_movement_declination(relationship, from_item, to_item)


def calculate_aspect_movement_ecliptic(
        relationship: RelationshipSchema,
        from_item: Tuple[PointSchema, EventSchema],
        to_item: Tuple[PointSchema, EventSchema],
):
    """
    Calculates whether degree or declination aspects are applying or separating.

    - Sets ecliptic aspects' `movement` `days_until_exact`, `utc_date_of_exact`, and `local_date_of_exact`
      if there is an orb of aspect and both objects have a speed.

    :param relationship: The relationship between points to store calculations in.
    :param from_item: The starting point in the relationship, and the event it is from.
    :param to_item: The ending point in the relationship, and the event it is from.
    """

    calculate_degree_types_from_speed(
        relationship.ecliptic_aspect,
        (from_item[0].longitude_velocity, from_item[1]),
        (to_item[0].longitude_velocity, to_item[1]),
        relationship.ecliptic_aspect.orb
    )

    calculate_degree_types_from_speed(
        relationship.precession_corrected_aspect,
        (from_item[0].longitude_velocity, from_item[1]),
        (to_item[0].longitude_velocity, to_item[1]),
        relationship.precession_corrected_aspect.orb
    )


def calculate_aspect_movement_declination(
        relationship: RelationshipSchema,
        from_item: Tuple[PointSchema, EventSchema],
        to_item: Tuple[PointSchema, EventSchema],
):
    """
    Calculates whether degree or declination aspects are applying or separating.

    - Sets declination aspect's `movement` `days_until_exact`, `utc_date_of_exact`, and `local_date_of_exact`
      if there is an orb of aspect and both objects have a speed.

    :param relationship: The relationship between points to store calculations in.
    :param from_item: The starting point in the relationship, and the event it is from.
    :param to_item: The ending point in the relationship, and the event it is from.
    """

    to_velocity = to_item[0].declination_velocity
    aspect_orb = relationship.declination_aspect.orb

    if relationship.declination_aspect.type == AspectType.contraparallel \
            and to_velocity is not None and aspect_orb is not None:
        to_velocity *= -1
        aspect_orb *= -1

    calculate_degree_types_from_speed(
        relationship.declination_aspect,
        (from_item[0].declination_velocity, from_item[1]),
        (to_velocity, to_item[1]),
        aspect_orb
    )


def calculate_degree_types_from_speed(
        aspect: AspectSchema,
        from_item: Tuple[Optional[float], EventSchema],
        to_item: Tuple[Optional[float], EventSchema],
        orb: float
):
    """
    Calculates whether points are applying or separating.

    - Sets the aspect's `movement` `days_until_exact`, `utc_date_of_exact`, and `local_date_of_exact`
      if there is an orb of aspect and both objects have a speed.

    :param aspect: The aspect object to update.
    :param from_item: The starting speed in the relationship, and the chart it is from.
    :param to_item: The ending speed in the relationship, and the chart it is from.
    :param orb: The orb between the two points.
    """

    from_velocity, to_velocity, is_same_direction = calculate_degree_types_direction(from_item, to_item)

    if orb is None or from_velocity is None or to_velocity is None:
        return

    from_is_faster = from_velocity >= to_velocity
    relative_velocity = from_velocity - to_velocity
    approximate_days_until_exact = orb / relative_velocity

    if approximate_days_until_exact < 7:
        # Set the approximate days until exact and date exact, if less than 1 week.
        aspect.days_until_exact = approximate_days_until_exact

        from_event = from_item[1]
        to_event = to_item[1]
        time_delta = datetime.timedelta(days=approximate_days_until_exact)

        if from_event.type == EventType.transit:
            aspect.utc_date_of_exact = from_event.utc_date + time_delta
            aspect.local_date_of_exact = from_event.local_date + time_delta
        else:
            aspect.utc_date_of_exact = to_event.utc_date + time_delta
            aspect.local_date_of_exact = to_event.local_date + time_delta

    if orb >= 0 if from_is_faster else orb < 0:
        # If the orb is positive and first object is faster,
        # or the orb is negative and the second object is faster,
        # the aspect is applying.
        aspect.movement = AspectMovementType.applying if is_same_direction \
            else AspectMovementType.mutually_applying
    if orb >= 0 if not from_is_faster else orb < 0:
        # If the orb is positive and second object is faster,
        # or the orb is negative and the first object is faster,
        # the aspect is separating.
        aspect.movement = AspectMovementType.separating if is_same_direction \
            else AspectMovementType.mutually_separating


def calculate_degree_types_direction(
        from_item: Tuple[Optional[float], EventSchema],
        to_item: Tuple[Optional[float], EventSchema],
) -> Tuple[Optional[float], Optional[float], bool]:
    """
    Calculates whether points are moving in the direction.

    :param from_item: The starting speed in the relationship, and the chart it is from.
    :param to_item: The ending speed in the relationship, and the chart it is from.

    :return: The from speed, the to speed, and whether the points are moving in the same direction.
    """

    from_velocity, from_event = from_item
    to_velocity, to_event = to_item

    # If aspects are between a transit chart and a base chart,
    # set the base speed to 0 and assert that the bodies are moving in the same direction.
    if from_event.type == EventType.transit and to_event.type != EventType.transit:
        return from_velocity, 0, True
    elif to_event.type == EventType.transit and from_event.type != EventType.transit:
        return 0, to_velocity, True
    elif not from_velocity or not to_velocity:
        return from_velocity, to_velocity, True

    return from_velocity, to_velocity, (from_velocity > 0) == (to_velocity > 0)
