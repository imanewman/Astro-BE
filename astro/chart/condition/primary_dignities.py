from astro.schema import PointSchema
from astro.util import point_traits


def calculate_primary_dignities(point: PointSchema):
    """
    Calculates the dignities of a planet based on its sign and house.

    - May set a points condition to `in_joy` when in its own house.
    - Planetary joys can be found at: https://theastrologydictionary.com/j/joys/

    - May set a point's condition to `in_domicile`, `in_exaltation`,
     `in_detriment`, or `fall`, when in the respective sign.
    - Essential dignities are based on this chart, with disputed
      outer planet conditions omitted: https://www.astro.com/astrowiki/en/Domicile

    :param point: The point to calculate the dignities for.
    """

    if point.name in point_traits.points:
        traits = point_traits.points[point.name]

        if traits.joy and traits.joy == point.house:
            point.condition.in_joy = True

        if point.sign in traits.domicile:
            point.condition.in_domicile = True

        if point.sign in traits.exaltation:
            point.condition.in_exaltation = True

        if point.sign in traits.detriment:
            point.condition.in_detriment = True

        if point.sign in traits.fall:
            point.condition.in_fall = True
