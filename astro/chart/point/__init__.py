from typing import Dict

from astro.util import Point
from astro.schema import PointSchema, SettingsSchema, EventSettingsSchema
from .ephemeris import get_julian_day
from .point_attributes import calculate_point_attributes
from .point_factory import create_points


def create_points_with_attributes(
        event_settings: EventSettingsSchema,
        settings: SettingsSchema = SettingsSchema()
) -> Dict[Point, PointSchema]:
    """
    Creates a mapping from all point names to that point's attributes at the given time and location.

    :param event_settings: The current time, location, and enabled points.
    :param settings: Settings used for calculations.

    :return: The calculated points.
    """

    # Set the julian day for the time
    event_settings.event.julian_day = get_julian_day(event_settings.event.utc_date)

    points = create_points(event_settings.event, event_settings.enabled_points)

    # Calculate the derived point attributes for each point.
    for point in points.values():
        calculate_point_attributes(point, settings.stationary_pct_of_avg_speed)

    return points
