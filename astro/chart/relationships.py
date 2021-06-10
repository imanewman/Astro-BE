from typing import List, Tuple

from astro.schema import AspectOrbs, PointInTime, PointRelationship
from astro.util import Point, aspectTraits, AspectType, PhaseType, point_traits


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
            calculate_aspect_phase(relationship, from_point, to_point)
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
    """

    # The relative degrees between two points
    absolute_degrees_between = \
        round(abs(from_point.degrees_from_aries - to_point.degrees_from_aries), 2)
    aspect_to_orb = orbs.aspect_to_orb()

    for aspect_type, aspect in aspectTraits.aspects.items():
        # for each type of aspect, calculate whether the degrees of separation between points
        # is within the orb of the degrees for this aspect.
        for orb in calculate_aspect_orbs(aspect.degrees, absolute_degrees_between):
            if abs(orb) <= aspect_to_orb[aspect_type]:
                relationship.degree_aspect = aspect_type
                relationship.degree_aspect_orb = orb

                break


def calculate_aspect_phase(
        relationship: PointRelationship,
        from_point: PointInTime,
        to_point: PointInTime,
):
    """
    Calculates the current separation in degrees, and the phase of that separation from
    the slower to the faster moving body, mapping the degrees out of 360 to 8 equal phases.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    """

    # Set a placeholder degrees between in case one of the points doesn't have a speed
    relationship.degrees_between = calculate_degrees_between(from_point, to_point)

    if from_point.name not in point_traits.points or to_point.name not in point_traits.points:
        return

    from_speed = point_traits.points[from_point.name].speed_avg
    to_speed = point_traits.points[to_point.name].speed_avg

    if not from_speed or not to_speed:
        return

    # find which body has the slower speed, which is used as the fulcrum
    slower, faster = (from_point, to_point) if from_speed < to_speed else (to_point, from_point)

    relationship.phase_base_point = slower.name
    relationship.degrees_between = calculate_degrees_between(slower, faster)

    # set the respective phase of the planets
    if relationship.degrees_between < 45:
        relationship.phase = PhaseType.new
    elif 45 <= relationship.degrees_between < 90:
        relationship.phase = PhaseType.crescent
    elif 90 <= relationship.degrees_between < 135:
        relationship.phase = PhaseType.first_quarter
    elif 135 <= relationship.degrees_between < 180:
        relationship.phase = PhaseType.gibbous
    elif 180 <= relationship.degrees_between < 225:
        relationship.phase = PhaseType.full
    elif 225 <= relationship.degrees_between < 270:
        relationship.phase = PhaseType.disseminating
    elif 270 <= relationship.degrees_between < 315:
        relationship.phase = PhaseType.last_quarter
    elif 315 <= relationship.degrees_between:
        relationship.phase = PhaseType.balsamic


def calculate_degrees_between(slower: PointInTime, faster: PointInTime) -> float:
    """
    calculate the degrees of phase from the slower to the faster planet.

    :param slower: The point to calculate degrees from.
    :param faster: The point to calculate degrees to.
    :return: The degrees out of 360 from the slower to the faster planet.
    """
    if slower.degrees_from_aries > faster.degrees_from_aries:
        return round(360 + faster.degrees_from_aries - slower.degrees_from_aries, 2)
    else:
        return round(faster.degrees_from_aries - slower.degrees_from_aries, 2)


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
    """

    if from_point.declination is not None \
            and to_point.declination is not None \
            and not (from_point.name == Point.north_mode and to_point.name == Point.south_node):
        parallel_orb = round(abs(from_point.declination - to_point.declination), 2)
        contraparallel_orb = round(abs(from_point.declination + to_point.declination), 2)

        relationship.declination_between = parallel_orb

        if parallel_orb <= orbs.parallel:
            relationship.declination_aspect = AspectType.parallel
            relationship.declination_aspect_orb = parallel_orb

        elif contraparallel_orb <= orbs.contraparallel:
            relationship.declination_aspect = AspectType.contraparallel
            relationship.declination_aspect_orb = contraparallel_orb


