from datetime import timedelta
from typing import List, Tuple

from astro import calculate_relationships
from astro.chart.point import create_points_with_attributes
from astro.schema import EventSettingsSchema, PointSchema, SettingsSchema, RelationshipSchema


def calculate_transits(
        event_settings: EventSettingsSchema,
        points: List[PointSchema]
):
    """
    Calculates the timing of transits for an event.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param points: The calculated points for this event.

    :return:
    """
    transit_settings = event_settings.transits

    if transit_settings.start_date > transit_settings.end_date \
            or not transit_settings.do_calculate_tropical \
            and not transit_settings.do_calculate_precession_corrected:
        return

    calculated_increments = []
    current_date = transit_settings.start_date
    settings = SettingsSchema(
        do_calculate_point_attributes=False,
        do_calculate_relationship_attributes=False,
    )

    while current_date < transit_settings.end_date:
        current_event = EventSettingsSchema(
            event={"utc_date": current_date}
        )
        current_points = create_points_with_attributes(
            current_event,
            settings
        )
        current_relationships = calculate_relationships(
            (points, event_settings),
            ([point for point in current_points.values()], current_event),
            False,
            settings
        )

        calculated_increments.append((current_event, current_relationships))

        current_date += timedelta(hours=1)

    calculate_transit_timing(calculated_increments)


def calculate_transit_timing(
        calculated_increments: List[Tuple[EventSettingsSchema, List[RelationshipSchema]]]
):
    """
    Calculates the timing of transits going exact.

    :param calculated_increments: The relationships calculated over the set duration.

    :return:
    """
    last_orbs = []

    for event_settings, relationships in calculated_increments:
        current_orbs = list(map(
            lambda rel: rel.ecliptic_aspect.orb,
            relationships
        ))

        # TODO: see which orbs change polarity.

        last_orbs = current_orbs
