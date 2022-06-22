from typing import List, Tuple, Dict

from astro.schema import EventSettingsSchema, RelationshipSchema, TransitGroupSchema, PointSchema
from astro.util import Point
from .group_transits import group_transits
from .time_aspects import calculate_all_aspects_timing
from .time_points import calculate_all_points_timing


Increment = Tuple[
    EventSettingsSchema,
    Dict[Point, PointSchema],
    Dict[str, RelationshipSchema]
]


def calculate_transit_timing(
        event_settings: EventSettingsSchema,
        calculated_increments: List[Increment],
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
    last_points = {}
    transits = []

    for current_event_settings, current_points, current_relationships in calculated_increments:
        for transit in calculate_all_points_timing(
                event_settings, current_event_settings,
                current_points, last_points,
                is_one_chart
        ):
            transits.append(transit)

        for transit in calculate_all_aspects_timing(
            event_settings, current_event_settings,
            current_relationships, last_relationships,
            is_one_chart
        ):
            transits.append(transit)

        last_relationships = current_relationships
        last_points = current_points

    return group_transits(event_settings, transits)
