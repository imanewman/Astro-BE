from typing import List

from astro.schema import TransitGroupSchema, TransitIncrement, EventSettingsSchema
from .group_transits import group_transits
from .time_aspects import calculate_all_aspects_timing
from .time_points import calculate_all_points_timing


def calculate_transit_timing(
        base_event_settings: EventSettingsSchema,
        calculated_increments: List[TransitIncrement]
) -> List[TransitGroupSchema]:
    """
    Calculates the timing of transits going exact.

    :param base_event_settings: The base event settings.
    :param calculated_increments: The relationships calculated over the set duration.

    :return: All calculated transits.
    """
    last_increment = (base_event_settings, {}, {})
    transits = []

    for increment in calculated_increments:
        transits += [
            *calculate_all_points_timing(base_event_settings, increment, last_increment),
            *calculate_all_aspects_timing(base_event_settings, increment, last_increment)
        ]

        last_increment = increment

    return group_transits(base_event_settings, transits)
