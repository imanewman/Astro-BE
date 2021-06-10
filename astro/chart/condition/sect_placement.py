from astro.schema import PointSchema
from astro.util import Point, SectPlacement


def calculate_sect_placement(point: PointSchema, is_day_time: bool):
    """
    Calculates whether this planet is benefic, malefic, or the sect light.

    - If the point Sun or the Moon at the right time of day, sets the `sect_placement` as the sect light.
    - If this point is Venus, Mars, Jupiter, and Saturn, sets the `sect_placement` as a benefic or
      malefic planet in or contrary to sect.

    :param point: The point to calculate the sect placement of.
    :param is_day_time: Whether the point is found during the day.
    """

    if (is_day_time and point.name == Point.sun) or \
            (not is_day_time and point.name == Point.moon):
        point.condition.sect_placement = SectPlacement.sect_light

    if point.name == Point.jupiter:
        point.condition.sect_placement = \
            SectPlacement.benefic_by_sect if is_day_time else SectPlacement.benefic_contrary_sect

    if point.name == Point.venus:
        point.condition.sect_placement = \
            SectPlacement.benefic_contrary_sect if is_day_time else SectPlacement.benefic_by_sect

    if point.name == Point.mars:
        point.condition.sect_placement = \
            SectPlacement.malefic_contrary_sect if is_day_time else SectPlacement.malefic_by_sect

    if point.name == Point.saturn:
        point.condition.sect_placement = \
            SectPlacement.malefic_by_sect if is_day_time else SectPlacement.malefic_contrary_sect
