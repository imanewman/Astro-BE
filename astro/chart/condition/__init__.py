from typing import Dict

from astro.schema import PointSchema, AspectOrbsSchema, SettingsSchema
from astro.util import Point
from .divisions import calculate_divisions
from .primary_dignities import calculate_primary_dignities
from .sect_placement import calculate_sect_placement
from .sun_conjunctions import calculate_sun_conjunctions
from .triplicity import calculate_triplicity


def calculate_condition(
        points: Dict[Point, PointSchema],
        is_day_time: bool,
        settings: SettingsSchema = SettingsSchema()
):
    """
    Calculates the conditions of bonification and maltreatment of relevant planets within the given points.

    - Sets attributes within each point's `division` and `condition`.

    :param points: The points to calculate the dignities for.
    :param is_day_time: Whether the points given are during the day.
    :param settings: The settings to use in calculations.
    """
    if not settings.do_calculate_condition:
        return

    for point in points.values():
        calculate_primary_dignities(point)
        calculate_sect_placement(point, is_day_time)

        if Point.sun in points:
            use_given_orbs = len(settings.events) > 0 and len(settings.events[0].enabled) > 0
            orbs = settings.events[0].enabled[0].orbs if use_given_orbs else AspectOrbsSchema()

            calculate_sun_conjunctions(point, points[Point.sun], orbs)

        if settings.do_calculate_divisions:
            calculate_triplicity(point, is_day_time)
            calculate_divisions(point)
