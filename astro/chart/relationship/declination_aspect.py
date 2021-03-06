from astro.schema import RelationshipSchema, PointSchema, SettingsSchema, EnabledPointsSchema
from astro.util import AspectType, point_axis_list


def calculate_declination_aspect(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
        enabled_settings: EnabledPointsSchema() = EnabledPointsSchema()
):
    """
    Calculates the declination degrees between and declination aspect between points.

    - If either point has no declination, or the points form an axis, no calculations are done.
    - Sets the relationship's `declination_arc`, `declination_aspect.type`,
      and `declination_aspect.orb` attributes.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param enabled_settings: The settings to use for calculations.
    """
    if from_point.declination is None \
            or to_point.declination is None \
            or [from_point.name, to_point.name] in point_axis_list \
            or [to_point.name, from_point.name] in point_axis_list:
        # Dont calculate aspects with no declination or for an axis.
        return

    parallel_orb = to_point.declination - from_point.declination
    contraparallel_orb = from_point.declination + to_point.declination

    relationship.declination_arc = parallel_orb

    if AspectType.parallel in enabled_settings.aspects and \
            abs(parallel_orb) <= enabled_settings.orbs.parallel:
        relationship.declination_aspect.type = AspectType.parallel
        relationship.declination_aspect.orb = parallel_orb

    elif AspectType.contraparallel in enabled_settings.aspects and \
            abs(contraparallel_orb) <= enabled_settings.orbs.contraparallel:
        relationship.declination_aspect.type = AspectType.contraparallel
        relationship.declination_aspect.orb = contraparallel_orb
