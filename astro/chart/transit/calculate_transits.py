from datetime import timedelta
from typing import List, Tuple

from astro.chart.relationship import calculate_relationships
from astro.chart.point import create_points_with_attributes
from astro.schema import EventSettingsSchema, PointSchema, SettingsSchema, TransitGroupSchema, TransitIncrement
from astro.util import EventType
from .time_transits import calculate_transit_timing


def calculate_transits(
        event_settings: EventSettingsSchema,
        points: List[PointSchema]
) -> List[TransitGroupSchema]:
    """
    Calculates the timing of transits for an event.

    :param event_settings: The current event settings.
    :param points: The calculated points for this event.

    :return: All calculated transits.
    """
    calculated_increments = []
    transit_settings = event_settings.transits

    if not transit_settings or not transit_settings.do_calculate():
        return []

    transit_event = transit_settings.event
    current_settings = EventSettingsSchema(
        enabled=transit_settings.enabled,
        event={
            **transit_event.dict(),
            "local_date": transit_event.local_date.replace(minute=0, second=0, microsecond=0),
            "utc_date": transit_event.utc_date.replace(minute=0, second=0, microsecond=0),
            "type": EventType.transit
        }
    )

    while current_settings.event.utc_date < transit_event.utc_end_date:
        calculated_increments.append(create_increment(
            (points, event_settings),
            current_settings
        ))

        delta_increment = timedelta(hours=transit_settings.hours_per_poll)
        current_settings = EventSettingsSchema(
            enabled=transit_settings.enabled,
            event={
                **current_settings.event.dict(),
                "utc_date": current_settings.event.utc_date + delta_increment,
                "local_date": current_settings.event.local_date + delta_increment
            }
        )

    return calculate_transit_timing(
        event_settings,
        calculated_increments
    )


def create_increment(
        base_items: Tuple[List[PointSchema], EventSettingsSchema],
        event_settings: EventSettingsSchema
) -> TransitIncrement:
    """
    Generates the relationships for an increment of time.

    :param base_items: The base charts points and event.
    :param event_settings: The current event settings to calculate transits for.

    :return: The calculated event and relationships at the current time.
    """
    relationship_map = {}
    is_one_chart = base_items[1].transits.is_one_chart()
    settings = SettingsSchema(
        calculate_relationship_phase=False,
    )
    current_points = create_points_with_attributes(event_settings, settings)
    current_items = ([point for point in current_points.values()], event_settings)

    current_relationships = calculate_relationships(
        current_items,
        current_items if is_one_chart else base_items,
        is_one_chart,
        settings
    )

    for relationship in current_relationships:
        relationship_map[relationship.get_name()] = relationship

    return event_settings, current_points, relationship_map
