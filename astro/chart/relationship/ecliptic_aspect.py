from typing import Tuple

from astro.schema import RelationshipSchema, PointSchema, SettingsSchema
from astro.collection import aspectTraits
from astro.util import point_axis_list


def calculate_ecliptic_aspect(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
        settings: SettingsSchema = SettingsSchema()
):
    """
    Calculates thee arc and degree based aspect between 2 points.

    - If a degree based aspect is in orb, sets the relationship's
      `ecliptic_aspect.type`, `ecliptic_aspect.orb`, and `ecliptic_aspect.angle` attributes.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param settings: The settings to use for calculations.
    """

    if [from_point.name, to_point.name] in point_axis_list \
            or [to_point.name, from_point.name] in point_axis_list:
        # Dont calculate aspects for an axis.
        return

    # Find the relative degrees from the faster to the slower point.
    absolute_arc_between = calculate_arc_between(relationship, from_point, to_point)

    aspect_to_orb = settings.orbs.aspect_to_orb()

    for aspect_type, aspect in aspectTraits.aspects.items():
        if aspect_type not in settings.enabled_aspects:
            return

        # For each type of aspect, calculate whether the degrees of separation between points
        # is within the orb of the degrees for this aspect.
        for orb in calculate_aspect_orbs(aspect.degrees, absolute_arc_between):
            if abs(orb) <= aspect_to_orb[aspect_type]:
                relationship.ecliptic_aspect.type = aspect_type
                relationship.ecliptic_aspect.orb = orb
                relationship.ecliptic_aspect.angle = aspect.degrees

                break


def calculate_arc_between(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
) -> float:
    """
    Calculates the arc from a faster planet to a slower planet.

    - If either planet has no speed, defaults to starting with `from_point`.
    - Sets the `relationship`'s `arc_between` to the smaller arc between the points.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.

    :return: The relative degrees from the faster to the slower point.
    """

    # Find the relative degrees from the first to the second point.
    arc_between = (from_point.longitude - to_point.longitude) % 360

    # Set the smaller arc of relative degrees between the points.
    if arc_between > 180:
        relationship.arc_minimal = 360 - arc_between
    else:
        relationship.arc_minimal = arc_between

    return arc_between


def calculate_aspect_orbs(aspect_degrees: float, degrees_of_separation: float) -> Tuple[float, float]:
    """
    Calculates the orbs between an aspect of the given amount of degrees and actual degrees of separation
    between points.

    :param aspect_degrees: The degrees corresponding to an exact aspect, such as 180 for an opposition.
    :param degrees_of_separation: The absolute degrees of separation between the planets.

    :return: The two orbs of separation for this aspect.
    """

    return (
        360 - aspect_degrees - degrees_of_separation,
        aspect_degrees - degrees_of_separation,
    )
