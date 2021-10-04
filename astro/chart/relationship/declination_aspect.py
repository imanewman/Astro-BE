from astro.schema import RelationshipSchema, PointSchema, AspectOrbsSchema
from astro.util import Point, AspectType, point_axis_list


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

    if from_point.declination is None \
            or to_point.declination is None \
            or [from_point.name, to_point.name] in point_axis_list \
            or [to_point.name, from_point.name] in point_axis_list:
        return

    parallel_orb = to_point.declination - from_point.declination
    contraparallel_orb = from_point.declination + to_point.declination

    relationship.declination_between = parallel_orb

    if abs(parallel_orb) <= orbs.parallel:
        relationship.declination_aspect = AspectType.parallel
        relationship.declination_aspect_orb = parallel_orb

    elif abs(contraparallel_orb) <= orbs.contraparallel:
        relationship.declination_aspect = AspectType.contraparallel
        relationship.declination_aspect_orb = contraparallel_orb
