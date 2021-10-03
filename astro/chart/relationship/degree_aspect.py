from typing import Tuple

from astro.schema import RelationshipSchema, PointSchema, AspectOrbsSchema
from astro.collection import aspectTraits


def calculate_degree_aspect(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
        orbs: AspectOrbsSchema = AspectOrbsSchema(),
):
    """
    Calculates thee arc and degree based aspect between 2 points.

    - If a degree based aspect is in orb, sets the relationship's
      `degree_aspect` and `degree_aspect_orb` attribute.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param orbs: The orbs to use for calculations.
    """

    # Find the relative degrees from the faster to the slower point.
    absolute_arc_between = calculate_arc_between(relationship, from_point, to_point)

    aspect_to_orb = orbs.aspect_to_orb()

    for aspect_type, aspect in aspectTraits.aspects.items():
        # For each type of aspect, calculate whether the degrees of separation between points
        # is within the orb of the degrees for this aspect.
        for orb in calculate_aspect_orbs(aspect.degrees, absolute_arc_between):
            if abs(orb) <= aspect_to_orb[aspect_type]:
                relationship.degree_aspect = aspect_type
                relationship.degree_aspect_orb = orb
                relationship.degree_aspect_angle = aspect.degrees

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
    arc_between = (from_point.degrees_from_aries - to_point.degrees_from_aries) % 360

    # Set the smaller arc of relative degrees between the points.
    if arc_between > 180:
        relationship.arc_between = 360 - arc_between
    else:
        relationship.arc_between = arc_between

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
