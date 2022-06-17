from datetime import timedelta
from typing import List, Tuple, Optional

from astro.chart.relationship import calculate_relationships
from astro.chart.point import create_points_with_attributes
from astro.schema import EventSettingsSchema, PointSchema, SettingsSchema, RelationshipSchema, AspectSchema


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
            or (not transit_settings.do_calculate_ecliptic
                and not transit_settings.do_calculate_declination
                and not transit_settings.do_calculate_precession_corrected):
        return

    calculated_increments = []
    current_date = transit_settings.start_date
    settings = SettingsSchema(
        do_calculate_point_attributes=False,
        do_calculate_relationship_attributes=False,
    )

    while current_date < transit_settings.end_date:
        current_event = EventSettingsSchema(
            event={"utc_date": current_date},
            enabled=transit_settings.enabled
        )
        current_points = create_points_with_attributes(
            current_event,
            settings
        )
        current_relationships = calculate_relationships(
            ([point for point in current_points.values()], current_event),
            (points, event_settings),
            False,
            settings
        )

        calculated_increments.append((current_event, current_relationships))

        current_date += timedelta(hours=1)

    calculate_transit_timing(event_settings, calculated_increments)


def calculate_transit_timing(
        event_settings: EventSettingsSchema,
        calculated_increments: List[Tuple[EventSettingsSchema, List[RelationshipSchema]]],
):
    """
    Calculates the timing of transits going exact.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param calculated_increments: The relationships calculated over the set duration.

    :return:
    """
    last_relationships = []

    for current_event_settings, current_relationships in calculated_increments:
        relationship_count = len(last_relationships)

        for relationship_index in range(relationship_count):
            last_relationship = last_relationships[relationship_index]
            current_relationship = current_relationships[relationship_index]

            def find_exact_aspect(last_aspect: AspectSchema, current_aspect: AspectSchema):
                if not last_aspect.orb or not current_aspect.orb:
                    return

                last_orb_is_positive = last_aspect.orb >= 0
                current_orb_is_positive = current_aspect.orb >= 0

                if (last_orb_is_positive and not current_orb_is_positive) \
                        or (current_orb_is_positive and not last_orb_is_positive):
                    print({
                        "from_point": last_relationship.from_point,
                        "to_point": last_relationship.to_point,
                        "type": last_aspect.type,
                        "is_precession_corrected": last_aspect.is_precession_corrected,
                        "last_orb": last_aspect.orb,
                        "current_orb": current_aspect.orb,
                        "current_utc_date": current_event_settings.event.utc_date.isoformat()
                    })

            if event_settings.transits.do_calculate_ecliptic:
                find_exact_aspect(
                    last_relationship.ecliptic_aspect,
                    current_relationship.ecliptic_aspect
                )
            if event_settings.transits.do_calculate_declination:
                find_exact_aspect(
                    last_relationship.declination_aspect,
                    current_relationship.declination_aspect
                )
            if event_settings.transits.do_calculate_precession_corrected:
                find_exact_aspect(
                    last_relationship.precession_corrected_aspect,
                    current_relationship.precession_corrected_aspect
                )

        last_relationships = current_relationships
