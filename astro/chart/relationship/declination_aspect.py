from astro.schema import RelationshipSchema, PointSchema, AspectOrbsSchema
from astro.util import Point, AspectType


def calculate_declination_aspect(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
        orbs: AspectOrbsSchema = AspectOrbsSchema(),
):
    """
    Calculates the declination degrees between and declination aspect between points.

    - If either point has no declination, or the points form an axis, no calculations are done.
    - Sets the relationship's `declination_between`, `declination_aspect`,
      and `declination_aspect_orb` attributes.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param orbs: The orbs to use for calculations.
    """

    if from_point.declination is not None \
            and to_point.declination is not None \
            and not (from_point.name == Point.north_mode and to_point.name == Point.south_node):
        parallel_orb = abs(from_point.declination - to_point.declination)
        contraparallel_orb = abs(from_point.declination + to_point.declination)

        relationship.declination_between = parallel_orb

        if parallel_orb <= orbs.parallel:
            relationship.declination_aspect = AspectType.parallel
            relationship.declination_aspect_orb = parallel_orb

        elif contraparallel_orb <= orbs.contraparallel:
            relationship.declination_aspect = AspectType.contraparallel
            relationship.declination_aspect_orb = contraparallel_orb
