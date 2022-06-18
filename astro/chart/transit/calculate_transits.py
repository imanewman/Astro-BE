from datetime import timedelta
from typing import List, Tuple, Optional, Dict

from astro.chart.relationship import calculate_relationships
from astro.chart.point import create_points_with_attributes
from astro.schema import EventSettingsSchema, PointSchema, SettingsSchema, RelationshipSchema, AspectSchema, \
    TransitSchema, TransitGroupSchema
from astro.util import TransitType, TransitGroupType


def calculate_transits(
        event_settings: EventSettingsSchema,
        points: List[PointSchema]
) -> List[TransitGroupSchema]:
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
    is_one_chart = transit_settings.type == TransitType.transit_to_transit
    current_settings = EventSettingsSchema(
        enabled=transit_settings.enabled,
        event=transit_settings.event
    )

    while current_settings.event.utc_date < transit_settings.event.utc_end_date:
        calculated_increments.append(create_increment(
            (points, event_settings),
            current_settings,
            is_one_chart
        ))

        current_settings = EventSettingsSchema(
            enabled=transit_settings.enabled,
            event={
                **current_settings.event.dict(),
                "utc_date": current_settings.event.utc_date + timedelta(hours=1),
                "local_date": current_settings.event.utc_date + timedelta(hours=1)
            }
        )

    return calculate_transit_timing(event_settings, calculated_increments, is_one_chart)


def create_increment(
        base_items: Tuple[List[PointSchema], EventSettingsSchema],
        event_settings: EventSettingsSchema,
        is_one_chart: bool
) -> Tuple[EventSettingsSchema, Dict[str, RelationshipSchema]]:
    """
    Generates the relationships for an increment of time.

    :param base_items: The base charts points and event.
    :param event_settings: The current event settings to calculate transits for.
    :param is_one_chart: If true, transits are calculated during the time frame, and not to the base chart.

    :return: The calculated event and relationships at the current time.
    """
    settings = SettingsSchema(
        do_calculate_point_attributes=False,
        do_calculate_relationship_phase=False,
    )
    current_points = create_points_with_attributes(
        event_settings,
        settings
    )
    current_items = ([point for point in current_points.values()], event_settings)

    current_relationships = calculate_relationships(
        current_items,
        current_items if is_one_chart else base_items,
        is_one_chart,
        settings
    )

    relationship_map = {}

    for relationship in current_relationships:
        relationship_map[relationship.get_name()] = relationship

    return event_settings, relationship_map


def calculate_transit_timing(
        event_settings: EventSettingsSchema,
        calculated_increments: List[Tuple[EventSettingsSchema, Dict[str, RelationshipSchema]]],
        is_one_chart: bool
) -> List[TransitGroupSchema]:
    """
    Calculates the timing of transits going exact.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param calculated_increments: The relationships calculated over the set duration.
    :param is_one_chart: If true, transits are calculated during the time frame, and not to the base chart.

    :return: All calculated transits.
    """
    last_relationships = {}
    transits = []

    for current_event_settings, current_relationships in calculated_increments:
        for last_relationship in last_relationships.values():
            current_relationship = current_relationships[last_relationship.get_name()]

            if not current_relationship:
                continue

            def find_transit(last: AspectSchema, current: AspectSchema):
                transit = find_exact_aspect(
                    current_event_settings,
                    current_relationship,
                    last,
                    current
                )
                if transit:
                    transits.append(transit)

            if event_settings.transits.do_calculate_ecliptic:
                find_transit(
                    last_relationship.ecliptic_aspect,
                    current_relationship.ecliptic_aspect
                )
            if event_settings.transits.do_calculate_declination:
                find_transit(
                    last_relationship.declination_aspect,
                    current_relationship.declination_aspect
                )
            if event_settings.transits.do_calculate_precession_corrected and not is_one_chart:
                find_transit(
                    last_relationship.precession_corrected_aspect,
                    current_relationship.precession_corrected_aspect
                )

        last_relationships = current_relationships

    return group_transits(event_settings, transits)


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


def group_transits(
        event_settings: EventSettingsSchema,
        transits: List[TransitSchema]
) -> List[TransitGroupSchema]:
    """
    Groups transits by shared fields.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param transits: The transits to group.

    :return: The grouped transits.
    """
    groups = {}

    if event_settings.transits.group_by == TransitGroupType.by_day:
        for transit in transits:
            day = transit.get_time().split(" ")[0]

            if day not in groups:
                groups[day] = TransitGroupSchema(
                    group_by=TransitGroupType.by_day,
                    group_value=day
                )

            groups[day].transits.append(transit)

    elif event_settings.transits.group_by == TransitGroupType.by_natal_point:
        for transit in transits:
            point = transit.to_point

            if point not in groups:
                groups[point] = TransitGroupSchema(
                    group_by=TransitGroupType.by_natal_point,
                    group_value=point
                )

            groups[point].transits.append(transit)

        return list(groups.values())

    elif event_settings.transits.group_by == TransitGroupType.by_transit_point:
        for transit in transits:
            point = transit.from_point

            if point not in groups:
                groups[point] = TransitGroupSchema(
                    group_by=TransitGroupType.by_transit_point,
                    group_value=point
                )

            groups[point].transits.append(transit)

    elif event_settings.transits.group_by == TransitGroupType.by_relationship:
        for transit in transits:
            relationship = transit.get_name()

            if relationship not in groups:
                groups[relationship] = TransitGroupSchema(
                    group_by=TransitGroupType.by_relationship,
                    group_value=relationship
                )

            groups[relationship].transits.append(transit)

        return list(groups.values())

    else:
        groups["all"] = TransitGroupSchema(transits=transits)

    return list(groups.values())
