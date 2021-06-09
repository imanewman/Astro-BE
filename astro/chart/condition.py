from typing import Dict

from astro.chart.relationships import calculate_aspect_orbs
from astro.schema import PointInTime, AspectOrbs
from astro.util import Point, point_traits, zodiac_sign_traits, SectPlacement, AspectType


def calculate_condition(
        points: Dict[Point, PointInTime],
        is_day_time: bool,
        orbs: AspectOrbs = AspectOrbs()
):
    """
    Calculates the conditions of bonification and maltreatment of relevant planets within the given points.

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


def calculate_primary_dignities(point: PointInTime):
    """
    Calculates the conditions of domicile, exaltation, detriment and fall for a given point.
    Also calculates whether the planet is in its joy.

    :param point: The point to calculate the dignities for.
    """

    if point.name in point_traits.points:
        traits = point_traits.points[point.name]

        if traits.joy and traits.joy == point.house:
            point.condition.in_joy = True

        if point.sign in traits.domicile:
            point.condition.in_domicile = True

        if point.sign in traits.exaltation:
            point.condition.in_exaltation = True

        if point.sign in traits.detriment:
            point.condition.in_detriment = True

        if point.sign in traits.fall:
            point.condition.in_fall = True


def calculate_sect_placement(point: PointInTime, is_day_time: bool):
    """
    Calculates whether this planet is benefic, malefic, or the sect light.

    :param point: The point to calculate the status for.
    :param is_day_time: Whether the points given are during the day, which affects the more significant planets.
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


def calculate_sun_conjunctions(point: PointInTime, sun: PointInTime, orbs: AspectOrbs = AspectOrbs()):
    """
    Calculates whether the point is under the beams, combust, or cazimi the sun.

    :param point: The point to check the proximity to the sun for.
    :param sun: The sun at the current time.
    :param orbs: The orbs to use for calculations of proximity.
    """

    # The relative degrees between two points
    separation = abs(point.degrees_from_aries - sun.degrees_from_aries)

    for orb in calculate_aspect_orbs(0, separation):
        if abs(orb) <= orbs.sun_cazimi_orb:
            point.condition.is_cazimi = True

        elif abs(orb) <= orbs.sun_combust_orb:
            point.condition.is_combust = True

        elif abs(orb) <= orbs.sun_under_beams_orb:
            point.condition.is_under_beams = True


def calculate_triplicity(point: PointInTime, is_day_time: bool):
    """
    Calculates the triplicity rulers for the given planet.

    :param point: The point to calculate the triplicity rulers for.
    :param is_day_time: Whether the points given are during the day, which affects the order of triplicity rulers.
    """

    traits = zodiac_sign_traits.signs[point.sign]

    point.condition.in_triplicity = point.name in traits.triplicity

    if is_day_time:
        point.rulers.triplicity = traits.triplicity
    else:
        point.rulers.triplicity = (traits.triplicity[1], traits.triplicity[0], traits.triplicity[2])


def calculate_divisions(point: PointInTime):
    """
    Calculates the division rulers for the given planet.

    :param point: The point to calculate the division rulers for.
    """

    traits = zodiac_sign_traits.signs[point.sign]

    point.rulers.sign = traits.rulership

    # Calculate bound ruler
    for bound in traits.bounds:
        if bound.from_degree <= point.degrees_in_sign < bound.to_degree:
            point.rulers.bound = bound.ruler

            if point.name == bound.ruler:
                point.condition.in_bound = True

    # Calculate decan ruler
    for decan in traits.decans:
        if decan.from_degree <= point.degrees_in_sign < decan.to_degree:
            point.rulers.decan = decan.ruler

            if point.name == decan.ruler:
                point.condition.in_decan = True
