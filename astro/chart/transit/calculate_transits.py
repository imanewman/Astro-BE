from datetime import timedelta
from typing import List, Tuple

from astro.chart.relationship import calculate_relationships
from astro.chart.point import create_points_with_attributes
from astro.schema import EventSettingsSchema, PointSchema, SettingsSchema, TransitGroupSchema
from astro.util import TransitCalculationType, EventType
from .time_transits import calculate_transit_timing, Increment


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
    is_one_chart = transit_settings.type == TransitCalculationType.transit_to_transit
    current_settings = EventSettingsSchema(
        enabled=transit_settings.enabled,
        event={
            **transit_settings.event.dict(),
            "local_date": transit_settings.event.local_date.replace(minute=0, second=0, microsecond=0),
            "utc_date": transit_settings.event.utc_date.replace(minute=0, second=0, microsecond=0),
            "type": EventType.transit
        }
    )

    while current_settings.event.utc_date < transit_settings.event.utc_end_date:
        calculated_increments.append(create_increment(
            (points, event_settings),
            current_settings,
            is_one_chart
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

    return calculate_transit_timing(event_settings, calculated_increments, is_one_chart)


def create_increment(
        base_items: Tuple[List[PointSchema], EventSettingsSchema],
        event_settings: EventSettingsSchema,
        is_one_chart: bool
) -> Increment:
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

    return event_settings, current_points, relationship_map
