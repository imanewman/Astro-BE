from datetime import timedelta, datetime
from typing import List, Tuple, Optional, Dict

from astro.chart.relationship import calculate_relationships
from astro.chart.point import create_points_with_attributes
from astro.schema import EventSettingsSchema, PointSchema, SettingsSchema, RelationshipSchema, AspectSchema, \
    TransitSchema


def calculate_transits(
        event_settings: EventSettingsSchema,
        points: List[PointSchema]
) -> List[TransitSchema]:
    """
    Calculates the timing of transits for an event.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param points: The calculated points for this event.

    :return: All calculated transits.
    """
    transit_settings = event_settings.transits

    if not transit_settings \
            or transit_settings.event.utc_date > transit_settings.event.utc_end_date \
            or (not transit_settings.do_calculate_ecliptic
                and not transit_settings.do_calculate_declination
                and not transit_settings.do_calculate_precession_corrected):
        return []

    calculated_increments = []
    current_utc_date = transit_settings.event.utc_date
    current_local_date = transit_settings.event.local_date

    while current_utc_date < transit_settings.event.utc_end_date:
        calculated_increments.append(create_increment(
            (points, event_settings),
            current_utc_date,
            current_local_date
        ))

        current_utc_date += timedelta(hours=1)
        current_local_date += timedelta(hours=1)

    return calculate_transit_timing(event_settings, calculated_increments)


def create_increment(
        base_items: Tuple[List[PointSchema], EventSettingsSchema],
        current_utc_date: datetime,
        current_local_date: datetime,
) -> Tuple[EventSettingsSchema, Dict[str, RelationshipSchema]]:
    """
    Generates the relationships for an increment of time.

    :param base_items: The base charts points and event.
    :param current_utc_date: The current UTC date to calculate transits for.
    :param current_local_date: The current local date to calculate transits for.

    :return: The calculated event and relationships at the current time.
    """
    settings = SettingsSchema(
        do_calculate_point_attributes=False,
        do_calculate_relationship_phase=False,
    )
    current_event = EventSettingsSchema(
        event={
            "utc_date": current_utc_date,
            "local_date": current_local_date
        },
        enabled=base_items[1].transits.enabled
    )
    current_points = create_points_with_attributes(
        current_event,
        settings
    )
    current_relationships = calculate_relationships(
        ([point for point in current_points.values()], current_event),
        base_items,
        False,
        settings
    )

    relationship_map = {}

    for relationship in current_relationships:
        relationship_map[relationship.get_name()] = relationship

    return current_event, relationship_map


def calculate_transit_timing(
        event_settings: EventSettingsSchema,
        calculated_increments: List[Tuple[EventSettingsSchema, Dict[str, RelationshipSchema]]],
) -> List[TransitSchema]:
    """
    Calculates the timing of transits going exact.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param calculated_increments: The relationships calculated over the set duration.

    :return: All calculated transits.
    """
    last_relationships = {}
    transits = []

    for current_event_settings, current_relationships in calculated_increments:
        for last_relationship in last_relationships.values():
            current_relationship = current_relationships[last_relationship.get_name()]

            if not current_relationship:
                continue

            if event_settings.transits.do_calculate_ecliptic:
                transit = find_exact_aspect(
                    current_event_settings, current_relationship,
                    last_relationship.ecliptic_aspect,
                    current_relationship.ecliptic_aspect
                )
                if transit:
                    transits.append(transit)
            if event_settings.transits.do_calculate_declination:
                transit = find_exact_aspect(
                    current_event_settings, current_relationship,
                    last_relationship.declination_aspect,
                    current_relationship.declination_aspect
                )
                if transit:
                    transits.append(transit)
            if event_settings.transits.do_calculate_precession_corrected:
                transit = find_exact_aspect(
                    current_event_settings, current_relationship,
                    last_relationship.precession_corrected_aspect,
                    current_relationship.precession_corrected_aspect
                )
                if transit:
                    transits.append(transit)

        last_relationships = current_relationships

    return transits


def find_exact_aspect(
    current_event_settings: EventSettingsSchema,
    current_relationship: RelationshipSchema,
    last_aspect: AspectSchema,
    current_aspect: AspectSchema
) -> Optional[TransitSchema]:
    """
    Finds an exact aspect between two moments in time.

    :param current_event_settings: The event for the current moment.
    :param current_relationship: The relationship between points in the current moment.
    :param last_aspect: The aspect between points in the last moment.
    :param current_aspect:  The aspect between points in the current moment.

    :return: The exact transit, if one exists.
    """
    if not last_aspect.orb or not current_aspect.orb:
        return

    last_orb_is_positive = last_aspect.orb >= 0
    current_orb_is_positive = current_aspect.orb >= 0
    aspect_is_same = last_aspect.type == current_aspect.type

    if aspect_is_same and last_orb_is_positive is not current_orb_is_positive:
        time_delta = current_aspect.get_approximate_timing()
        local_exact_date = current_event_settings.event.local_date + time_delta
        utc_exact_date = current_event_settings.event.utc_date + time_delta

        return TransitSchema(**{
            **current_aspect.dict(),
            "from_point": current_relationship.from_point,
            "to_point": current_relationship.to_point,
            "local_exact_date": local_exact_date,
            "utc_exact_date": utc_exact_date
        })
