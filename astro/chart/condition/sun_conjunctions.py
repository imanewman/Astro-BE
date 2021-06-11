from astro.chart.relationship.degree_aspect import calculate_aspect_orbs
from astro.schema import PointSchema, AspectOrbsSchema


def calculate_sun_conjunctions(point: PointSchema, sun: PointSchema, orbs: AspectOrbsSchema = AspectOrbsSchema()):
    """
    Calculates whether the point is under the beams, combust, or cazimi the sun.

    - Sets the point's condition to `is_cazimi` if within very close proximity.
    - Sets the point's condition to `is_combust` if within close proximity.
    - Sets the point's condition to `is_under_beams` if within invisible proximity.

    :param point: The point to check the proximity to the sun for.
    :param sun: The sun at the current time.
    :param orbs: The orbs to use for calculations of proximity.
    """

    # The relative degrees between two points
    separation = abs(point.degrees_from_aries - sun.degrees_from_aries)

    for orb in calculate_aspect_orbs(0, separation):
        if abs(orb) <= orbs.sun_cazimi_orb:
            point.condition.is_cazimi = True

        elif abs(orb) <= orbs.sun_combust_orb:
            point.condition.is_combust = True

        elif abs(orb) <= orbs.sun_under_beams_orb:
            point.condition.is_under_beams = True
