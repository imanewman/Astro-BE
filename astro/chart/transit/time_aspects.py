from typing import List, Optional

from astro.schema import RelationshipSchema, AspectSchema, TransitSchema, TransitIncrement, PointMap
from astro.util import AspectMovementType, TransitType


def calculate_all_aspects_timing(
        base_increment: TransitIncrement,
        current_increment: TransitIncrement,
        last_increment: TransitIncrement,
) -> List[TransitSchema]:
    """
    Calculates the timing of all transits going exact.

    :param base_increment: The base [0] event, [1] points, and [2] relationships.
    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param last_increment: The last [0] event, [1] points, and [2] relationships.

    :return: All calculated transits.
    """
    base_event_settings = base_increment[0]
    last_relationships, current_relationships = last_increment[2], current_increment[2]
    transits = []

    if not base_event_settings.transits.do_calculate_aspects():
        return transits

    for last_relationship in last_relationships.values():
        current_relationship = current_relationships[last_relationship.get_name()]

        if not current_relationship:
            continue

        for transit in calculate_aspect_timing(
                base_increment,
                current_increment,
                current_relationship,
                last_relationship
        ):
            transits.append(transit)

    return transits


def calculate_aspect_timing(
        base_increment: TransitIncrement,
        current_increment: TransitIncrement,
        current_relationship: RelationshipSchema,
        last_relationship: RelationshipSchema
) -> List[TransitSchema]:
    """
    Calculates the timing of transits going exact.

    :param base_increment: The base [0] event, [1] points, and [2] relationships.
    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_relationship: The current relationship between points.
    :param last_relationship: The previous relationship between points.

    :return: All calculated transits.
    """
    settings = base_increment[0].transits
    to_points = current_increment[1] if settings.is_one_chart()  else base_increment[1]
    transits = []

    def find_transit(last: AspectSchema, current: AspectSchema):
        transit = find_exact_aspect(
            current_increment,
            current_relationship,
            last,
            current,
            to_points
        )
        if transit:
            transits.append(transit)

    if settings.do_calculate_ecliptic:
        find_transit(
            last_relationship.ecliptic_aspect,
            current_relationship.ecliptic_aspect
        )
    if settings.do_calculate_declination:
        find_transit(
            last_relationship.declination_aspect,
            current_relationship.declination_aspect
        )
    if settings.do_calculate_precession_corrected and not settings.is_one_chart():
        find_transit(
            last_relationship.precession_corrected_aspect,
            current_relationship.precession_corrected_aspect
        )

    return transits


def find_exact_aspect(
        current_increment: TransitIncrement,
        current_relationship: RelationshipSchema,
        last_aspect: AspectSchema,
        current_aspect: AspectSchema,
        to_points: PointMap
) -> Optional[TransitSchema]:
    """
    Finds an exact aspect between two moments in time.

    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_relationship: The relationship between points in the current moment.
    :param last_aspect: The aspect between points in the last moment.
    :param current_aspect:  The aspect between points in the current moment.
    :param to_points:  The collection of points this aspect is to.

    :return: The exact transit, if one exists.
    """
    if not last_aspect.orb or not current_aspect.orb:
        return

    current_event_settings, current_points, current_relationships = current_increment
    last_orb_is_positive = last_aspect.orb >= 0
    current_orb_is_positive = current_aspect.orb >= 0
    aspect_is_same = last_aspect.type == current_aspect.type

    if aspect_is_same and (last_orb_is_positive is not current_orb_is_positive):
        time_delta = current_aspect.get_approximate_timing()
        local_exact_date = current_event_settings.event.local_date + time_delta
        utc_exact_date = current_event_settings.event.utc_date + time_delta
        name = f"{current_relationship.get_from()} {current_aspect.type} {current_relationship.get_to()}"
        from_point = current_points[current_relationship.from_point]
        to_point = to_points[current_relationship.from_point]

        return TransitSchema(
            **current_aspect.dict(exclude={"movement"}),
            from_type=current_relationship.from_type,
            to_type=current_relationship.to_type,
            from_point=from_point.name,
            to_point=to_point.name,
            from_sign=from_point.sign,
            to_sign=to_point.sign,
            name=name,
            movement=AspectMovementType.exact,
            transit_type=TransitType.aspect,
            local_exact_date=local_exact_date,
            utc_exact_date=utc_exact_date,
        )
