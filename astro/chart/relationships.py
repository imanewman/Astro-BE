from typing import List, Tuple

from astro.schema import AspectOrbs, PointInTime, PointRelationship
from astro.util import Point, aspectTraits, AspectType


def calculate_relationships(
        from_points: List[PointInTime],
        to_points: List[PointInTime],
        is_natal: bool = False,
        orbs: AspectOrbs = AspectOrbs(),
) -> List[PointRelationship]:
    """
   Calculates the relationships between each set of 2 points.

   :param from_points: The points to calculate aspects from.
   :param to_points: The points to calculate aspects to.
   :param orbs: The orbs to use for calculations.
   :param is_natal: If true, aspects will not be bi-directionally duplicated.

   :return: All calculated relationships.
   """

    aspects = []

    for from_point in from_points:
        if is_natal:
            # For natal charts, skip the points that have been calculated already to avoid duplicates.
            to_points = to_points[1:]

        for to_point in to_points:
            relationship = PointRelationship(
                from_point=from_point.name,
                to_point=to_point.name
            )

            calculate_sign_aspects(relationship, from_point, to_point)
            calculate_degree_aspects(relationship, from_point, to_point, orbs)
            calculate_declination_aspects(relationship, from_point, to_point, orbs)

            aspects.append(relationship)

    return aspects


def calculate_sign_aspects(
        relationship: PointRelationship,
        from_point: PointInTime,
        to_point: PointInTime
):
    """
    Calculates the sign based aspect between points.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :return:
    """

    if from_point.house is to_point.house:
        relationship.sign_aspect = AspectType.conjunction
    elif abs(from_point.house - to_point.house) == 6:
        relationship.sign_aspect = AspectType.opposition
    elif abs(from_point.house - to_point.house) in [4, 8]:
        relationship.sign_aspect = AspectType.trine
    elif abs(from_point.house - to_point.house) in [3, 9]:
        relationship.sign_aspect = AspectType.square
    elif abs(from_point.house - to_point.house) in [2, 10]:
        relationship.sign_aspect = AspectType.sextile
    else:
        relationship.sign_aspect = AspectType.aversion


def calculate_degree_aspects(
        relationship: PointRelationship,
        from_point: PointInTime,
        to_point: PointInTime,
        orbs: AspectOrbs = AspectOrbs(),
):
    """
    Calculates the degrees between, degree based aspect, and phase between points.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param orbs: The orbs to use for calculations.
    :return:
    """

    # The relative degrees between two points
    relationship.degrees_between = \
        round(abs(from_point.degrees_from_aries - to_point.degrees_from_aries), 2)
    aspect_to_orb = orbs.aspect_to_orb()

    for aspect_type, aspect in aspectTraits.aspects.items():
        # for each type of aspect, calculate whether the degrees of separation between points
        # is within the orb of the degrees for this aspect.
        for orb in calculate_aspect_orbs(aspect.degrees, relationship.degrees_between):
            if abs(orb) <= aspect_to_orb[aspect_type]:
                relationship.degree_aspect = aspect_type
                relationship.degree_aspect_orb = orb

                break


def calculate_aspect_orbs(aspect_degrees: float, degrees_of_separation: float) -> Tuple[float, float]:
    """
    Calculates the orbs between an aspect of the given amount of degrees and the actual degrees of separation
    between points.

    :param aspect_degrees: The degrees corresponding to an exact aspect, such as 180 for an opposition.
    :param degrees_of_separation: The degrees of separation between the planets.
    :return: The two orbs of separation for this aspect.
    """

    return (
        round(aspect_degrees - degrees_of_separation, 2),
        round(360 - aspect_degrees - degrees_of_separation, 2)
    )


def calculate_declination_aspects(
        relationship: PointRelationship,
        from_point: PointInTime,
        to_point: PointInTime,
        orbs: AspectOrbs = AspectOrbs(),
):
    """
    Calculates the declination degrees between and declination aspect between points.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param orbs: The orbs to use for calculations.
    :return:
    """

    if from_point.declination is not None \
            and to_point.declination is not None \
            and not (from_point.name == Point.north_mode and to_point.name == Point.south_node):
        parallel_orb = round(abs(from_point.declination - to_point.declination), 2)
        contraparallel_orb = round(abs(from_point.declination + to_point.declination), 2)

        if parallel_orb <= orbs.parallel:
            relationship.declination_aspect = AspectType.parallel
            relationship.declination_aspect_orb = parallel_orb

        elif contraparallel_orb <= orbs.contraparallel:
            relationship.declination_aspect = AspectType.contraparallel
            relationship.declination_aspect_orb = contraparallel_orb


