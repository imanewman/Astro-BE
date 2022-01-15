from typing import Tuple, Dict, Optional

from astro.schema import RelationshipSchema, PointSchema, SettingsSchema, EnabledPointsSchema
from astro.collection import aspect_traits
from astro.util import AspectType


def calculate_ecliptic_aspect(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
        enabled_settings: EnabledPointsSchema() = EnabledPointsSchema()
):
    """
    Calculates the arc and degree based aspect between 2 points.

    - If a degree based aspect is in orb, sets the relationship's
      `ecliptic_aspect.type`, `ecliptic_aspect.orb`, and `ecliptic_aspect.angle` attributes.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    :param enabled_settings: The settings to use for calculations.
    """
    absolute_arc_between = calculate_arc_between(relationship, from_point, to_point)

    aspect_type, orb, angle = calculate_ecliptic_aspect_type(
        absolute_arc_between,
        enabled_settings
    )

    relationship.ecliptic_aspect.type = aspect_type
    relationship.ecliptic_aspect.orb = orb
    relationship.ecliptic_aspect.angle = angle

    if relationship.precession_correction == 0:
        # Avoid rerunning calculations if there is no correction value.
        relationship.precession_corrected_aspect.type = aspect_type
        relationship.precession_corrected_aspect.orb = orb
        relationship.precession_corrected_aspect.angle = angle
    else:
        # Calculate the additional corrected aspect if there is a correction value.
        corrected_absolute_arc_between = absolute_arc_between + relationship.precession_correction
        corrected_aspect_type, corrected_orb, corrected_angle = calculate_ecliptic_aspect_type(
            corrected_absolute_arc_between,
            enabled_settings
        )

        relationship.precession_corrected_aspect.type = corrected_aspect_type
        relationship.precession_corrected_aspect.orb = corrected_orb
        relationship.precession_corrected_aspect.angle = corrected_angle


def calculate_ecliptic_aspect_type(
        absolute_arc_between: float,
        enabled_settings: EnabledPointsSchema() = EnabledPointsSchema()
) -> Tuple[Optional[AspectType], Optional[float], Optional[float]]:
    """
    Calculates the degree based aspect between 2 points.

    :param absolute_arc_between: The arc between two points.
    :param enabled_settings: The settings to use for calculations.

    :return:
        [0] The aspect type between the two points.
        [1] The aspect orb between the two points.
        [2] The aspect type's perfect degrees.
    """
    aspect_to_orb = enabled_settings.orbs.aspect_to_orb()

    for aspect_type, aspect in aspect_traits.aspects.items():
        if aspect_type not in enabled_settings.aspects:
            continue

        # For each type of aspect, calculate whether the degrees of separation between points
        # is within the orb of the degrees for this aspect.
        for orb in calculate_aspect_orbs(aspect.degrees, absolute_arc_between):
            if abs(orb) <= aspect_to_orb[aspect_type]:
                return aspect_type, orb, aspect.degrees

    return None, None, None


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
