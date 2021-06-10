from typing import Dict

from astro.util import Point
from astro.schema import EventSchema, PointSchema
from astro.chart.point.ephemeris import get_julian_day
from .point_attributes import calculate_point_attributes
from .point_factory import create_points


def create_points_with_attributes(
        event: EventSchema,
        stationary_pct_of_avg_speed: float = 0.3
) -> Dict[Point, PointSchema]:
    """
    Creates a mapping from all point names to that point's attributes at the given time and location.

    :param event: The current time and location.
    :param stationary_pct_of_avg_speed: The percent of the average speed of the point
     that a point must be under to be considered stationary.

    :return: The calculated points.
    """

    # Set the julian day for the time
    event.julian_day = get_julian_day(event.utc_date)

    points = create_points(event)

    # Calculate the derived point attributes for each point.
    for point in points.values():
        calculate_point_attributes(point, stationary_pct_of_avg_speed)

    return points
