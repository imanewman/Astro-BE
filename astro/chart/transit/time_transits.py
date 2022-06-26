from typing import List

from astro.schema import TransitGroupSchema, TransitIncrement
from .group_transits import group_transits
from .time_aspects import calculate_all_aspects_timing
from .time_points import calculate_all_points_timing


def calculate_transit_timing(
        base_increment: TransitIncrement,
        calculated_increments: List[TransitIncrement]
) -> List[TransitGroupSchema]:
    """
    Calculates the timing of transits going exact.

    :param base_increment: The base [0] event, [1] points, and [2] relationships.
    :param calculated_increments: The relationships calculated over the set duration.

    :return: All calculated transits.
    """
    event_settings = base_increment[0]
    last_increment = (event_settings, {}, {})
    transits = []

    for increment in calculated_increments:
        transits += [
            *calculate_all_points_timing(event_settings, increment, last_increment),
            *calculate_all_aspects_timing(base_increment, increment, last_increment)
        ]

        last_increment = increment

    return group_transits(event_settings, transits)
