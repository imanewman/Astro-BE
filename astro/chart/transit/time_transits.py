from typing import List, Tuple, Dict

from astro.schema import EventSettingsSchema, TransitGroupSchema
from .group_transits import group_transits
from .time_aspects import calculate_all_aspects_timing
from .time_points import calculate_all_points_timing
from ...schema.types import Increment


def calculate_transit_timing(
        event_settings: EventSettingsSchema,
        calculated_increments: List[Increment]
) -> List[TransitGroupSchema]:
    """
    Calculates the timing of transits going exact.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param calculated_increments: The relationships calculated over the set duration.

    :return: All calculated transits.
    """
    last_relationships = {}
    last_points = {}
    transits = []

    for current_event_settings, current_points, current_relationships in calculated_increments:
        transits += [
            *calculate_all_points_timing(
                event_settings, current_event_settings,
                current_points, last_points
            ),
            *calculate_all_aspects_timing(
                event_settings, current_event_settings,
                current_relationships, last_relationships
            )
        ]

        last_relationships = current_relationships
        last_points = current_points

    return group_transits(event_settings, transits)
