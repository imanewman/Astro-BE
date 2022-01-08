from astro.chart.relationship.ecliptic_aspect import calculate_aspect_orbs
from astro.schema import PointSchema, AspectOrbsSchema
from astro.util import SunCondition, Point


def calculate_sun_conjunctions(point: PointSchema, sun: PointSchema, orbs: AspectOrbsSchema = AspectOrbsSchema()):
    """
    Calculates whether the point is under the beams, combust, or cazimi the sun.

    - Sets the point's condition to `condition.sun_proximity` if with close proximity to the sun.

    :param point: The point to check the proximity to the sun for.
    :param sun: The sun at the current time.
    :param orbs: The orbs to use for calculations of proximity.
    """
    arc = abs(point.longitude - sun.longitude)

    if point.name == Point.sun:
        return

    for orb in calculate_aspect_orbs(0, arc):
        if abs(orb) <= orbs.sun_cazimi_orb:
            point.condition.sun_proximity = SunCondition.cazimi

        elif abs(orb) <= orbs.sun_combust_orb:
            point.condition.sun_proximity = SunCondition.combust

        elif abs(orb) <= orbs.sun_under_beams_orb:
            point.condition.sun_proximity = SunCondition.under_the_beams
