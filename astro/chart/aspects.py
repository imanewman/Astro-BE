from typing import List

from astro.schema import CalculatedAspects, AspectOrbs, PointInTime, AspectInTime
from astro.util import AspectType, Point, aspectTraits


def calculate_aspects(
        from_points: List[PointInTime],
        to_points: List[PointInTime],
        orbs: AspectOrbs,
        is_natal: bool
) -> CalculatedAspects:
    """
    Calculates all aspects between points.

    :param from_points: The points to calculate aspects from.
    :param to_points: The points to calculate aspects to.
    :param orbs: The orbs to use for calculations.
    :param is_natal: If true, aspects will not be duplicated.

    :return: All calculated aspects.
    """

    by_degree = calculate_degree_based_aspects(from_points, to_points, orbs, is_natal)

    return CalculatedAspects(
        by_degree=by_degree,
        by_sign_not_degree=calculate_sign_based_aspects(from_points, to_points, by_degree, is_natal),
        by_declination=calculate_declination_aspects(from_points, to_points, orbs, is_natal)
    )


def calculate_degree_based_aspects(
        from_points: List[PointInTime],
        to_points: List[PointInTime],
        orbs: AspectOrbs,
        is_natal: bool
) -> List[AspectInTime]:
    aspects = []

    aspect_to_orb = {
        AspectType.conjunction: orbs.conjunction,
        AspectType.opposition: orbs.opposition,
        AspectType.square: orbs.square,
        AspectType.trine: orbs.trine,
        AspectType.sextile: orbs.sextile,
        AspectType.quintile: orbs.quintile,
        AspectType.septile: orbs.septile,
        AspectType.octile: orbs.octile,
        AspectType.novile: orbs.novile,
        AspectType.semi_sextile: orbs.semi_sextile,
        AspectType.quincunx: orbs.quincunx,
        AspectType.sesquiquadrate: orbs.sesquiquadrate,
        AspectType.bi_quintile: orbs.bi_quintile,
    }

    for from_point in from_points:
        if is_natal:
            # For natal charts, skip the points that have been calculated already to avoid duplicates.
            to_points = to_points[1:]

        for to_point in to_points:
            separation = abs(from_point.degrees_from_aries - to_point.degrees_from_aries)

            for aspect_type, aspect in aspectTraits.aspects.items():
                orbs = [round(abs(aspect.degrees - separation), 2)]

                if aspect.name is AspectType.conjunction:
                    orbs.append(round(abs(separation - 360), 2))

                for orb in orbs:
                    if orb < aspect_to_orb[aspect_type]:
                        aspects.append(
                            AspectInTime(
                                type=aspect_type,
                                from_point=from_point.name,
                                to_point=to_point.name,
                                orb=orb
                            )
                        )

    return aspects


def calculate_sign_based_aspects(
        from_points: List[PointInTime],
        to_points: List[PointInTime],
        aspects_by_degree: List[AspectInTime],
        is_natal: bool
) -> List[AspectInTime]:
    aspects = []

    return aspects


def calculate_declination_aspects(
        from_points: List[PointInTime],
        to_points: List[PointInTime],
        orbs: AspectOrbs,
        is_natal: bool
) -> List[AspectInTime]:
    """
    Calculates aspects by declination.

    :param from_points: The points to calculate aspects from.
    :param to_points: The points to calculate aspects to.
    :param orbs: The orbs to use for calculations.
    :param is_natal: If true, aspects will not be duplicated.

    :return: All declination aspects
    """
    aspects = []

    for from_point in from_points:
        if is_natal:
            # For natal charts, skip the points that have been calculated already to avoid duplicates.
            to_points = to_points[1:]

        for to_point in to_points:
            if from_point.declination and to_point.declination \
                    and not (from_point.name == Point.north_mode and to_point.name == Point.south_node):
                parallel_orb = round(abs(from_point.declination - to_point.declination), 2)
                contraparallel_orb = round(abs(from_point.declination + to_point.declination), 2)

                if parallel_orb < orbs.parallel:
                    aspects.append(
                        AspectInTime(
                            type=AspectType.parallel,
                            from_point=from_point.name,
                            to_point=to_point.name,
                            orb=parallel_orb
                        )
                    )

                elif contraparallel_orb < orbs.contraparallel:
                    aspects.append(
                        AspectInTime(
                            type=AspectType.contraparallel,
                            from_point=from_point.name,
                            to_point=to_point.name,
                            orb=contraparallel_orb
                        )
                    )

    return aspects
