from typing import Dict

from astro.schema import PointSchema, AspectOrbs
from astro.util import Point
from .divisions import calculate_divisions
from .primary_dignities import calculate_primary_dignities
from .sect_placement import calculate_sect_placement
from .sun_conjunctions import calculate_sun_conjunctions
from .triplicity import calculate_triplicity


def calculate_condition(
        points: Dict[Point, PointSchema],
        is_day_time: bool,
        orbs: AspectOrbs = AspectOrbs()
):
    """
    Calculates the conditions of bonification and maltreatment of relevant planets within the given points.

    - Sets attributes within each point's `rulers` and `condition`.

    :param points: The points to calculate the dignities for.
    :param is_day_time: Whether the points given are during the day.
    :param orbs: The orbs to use for checking proximity of points to the sun.
    """

    for point in points.values():
        calculate_primary_dignities(point)
        calculate_sect_placement(point, is_day_time)
        calculate_triplicity(point, is_day_time)
        calculate_divisions(point)
        calculate_sun_conjunctions(point, points[Point.sun], orbs)