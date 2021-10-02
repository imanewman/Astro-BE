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
    Calculates the degrees between and degree based aspect between 2 points.

    - If a degree based aspect is in orb, sets the relationship's
      `degree_aspect` and `degree_aspect_orb` attribute.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param orbs: The orbs to use for calculations.
    """

    # The relative degrees between two points.
    absolute_degrees_between = abs(from_point.degrees_from_aries - to_point.degrees_from_aries)

    # Make sure to use the minimal relative degrees between the points.
    if absolute_degrees_between > 180:
        relationship.degrees_between = -(360 - absolute_degrees_between)
    else:
        relationship.degrees_between = absolute_degrees_between

    aspect_to_orb = orbs.aspect_to_orb()

    for aspect_type, aspect in aspectTraits.aspects.items():
        # For each type of aspect, calculate whether the degrees of separation between points
        # is within the orb of the degrees for this aspect.
        for orb in calculate_aspect_orbs(aspect.degrees, absolute_degrees_between):
            if abs(orb) <= aspect_to_orb[aspect_type]:
                relationship.degree_aspect = aspect_type
                relationship.degree_aspect_orb = orb
                relationship.degree_aspect_angle = aspect.degrees

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
        aspect_degrees - degrees_of_separation,
        360 - aspect_degrees - degrees_of_separation
    )
