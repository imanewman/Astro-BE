from typing import List, Optional

from astro.schema import RelationshipSchema, AspectSchema, TransitSchema, TransitIncrement, EventSettingsSchema
from astro.util import AspectMovementType, TransitType


def calculate_all_aspects_timing(
        base_event_settings: EventSettingsSchema,
        current_increment: TransitIncrement,
        last_increment: TransitIncrement,
) -> List[TransitSchema]:
    """
    Calculates the timing of all transits going exact.

    :param base_event_settings: The base event settings.
    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param last_increment: The last [0] event, [1] points, and [2] relationships.

    :return: All calculated transits.
    """
    last_relationships, current_relationships = last_increment[2], current_increment[2]
    transits = []

    if not base_event_settings.transits.do_calculate_aspects():
        return transits

    for last_relationship in last_relationships.values():
        current_relationship = current_relationships[last_relationship.get_name()]

        if not current_relationship:
            continue

        for transit in calculate_aspect_timing(
                base_event_settings,
                current_increment,
                current_relationship,
                last_relationship
        ):
            transits.append(transit)

    return transits


def calculate_aspect_timing(
        base_event_settings: EventSettingsSchema,
        current_increment: TransitIncrement,
        current_relationship: RelationshipSchema,
        last_relationship: RelationshipSchema
) -> List[TransitSchema]:
    """
    Calculates the timing of transits going exact.

    :param base_event_settings: The base event settings.
    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_relationship: The current relationship between points.
    :param last_relationship: The previous relationship between points.

    :return: All calculated transits.
    """
    settings = base_event_settings.transits
    transits = []

    def find_transit(last: AspectSchema, current: AspectSchema):
        transit = find_exact_aspect(
            current_increment,
            current_relationship,
            last,
            current
        )
        if transit:
            transits.append(transit)

    if settings.calculate_ecliptic:
        find_transit(
            last_relationship.ecliptic_aspect,
            current_relationship.ecliptic_aspect
        )
    if settings.calculate_declination:
        find_transit(
            last_relationship.declination_aspect,
            current_relationship.declination_aspect
        )
    if settings.calculate_precession_corrected and not settings.is_one_chart():
        find_transit(
            last_relationship.precession_corrected_aspect,
            current_relationship.precession_corrected_aspect
        )

    return transits


def find_exact_aspect(
        current_increment: TransitIncrement,
        current_relationship: RelationshipSchema,
        last_aspect: AspectSchema,
        current_aspect: AspectSchema
) -> Optional[TransitSchema]:
    """
    Finds an exact aspect between two moments in time.

    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_relationship: The relationship between points in the current moment.
    :param last_aspect: The aspect between points in the last moment.
    :param current_aspect:  The aspect between points in the current moment.

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
        name = f"({current_relationship.get_from()}) {current_aspect.type} ({current_relationship.get_to()})"

        return TransitSchema(
            **current_aspect.dict(exclude={"movement"}),
            from_type=current_relationship.from_type,
            to_type=current_relationship.to_type,
            from_point=current_relationship.from_point,
            to_point=current_relationship.to_point,
            from_sign=current_relationship.from_sign,
            to_sign=current_relationship.to_sign,
            name=name,
            movement=AspectMovementType.exact,
            transit_type=TransitType.aspect,
            local_exact_date=local_exact_date,
            utc_exact_date=utc_exact_date,
        )
