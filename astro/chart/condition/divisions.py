from astro.schema import PointSchema
from astro.collection.zodiac_sign_traits import zodiac_sign_traits


def calculate_divisions(point: PointSchema):
    """
    Calculates the bound and decan division rulers for the given planet.

    - Sets the point's `rulers.bound` to the bound ruler of the division of the sign
      that the point is within.
    - If the point is in its own bound, sets its condition to `in_bound`.
    - Sets the point's `rulers.decan` to the decan ruler of the division of the sign
      that the point is within.
    - If the point is in its own decan, sets its condition to `in_decan`.

    :param point: The point to calculate the division rulers for.
    """

    traits = zodiac_sign_traits.signs[point.sign]

    point.rulers.sign = traits.rulership

    # Calculate bound ruler
    for bound in traits.bounds:
        if bound.from_degree <= point.degrees_in_sign < bound.to_degree:
            point.rulers.bound = bound.ruler

            if point.name == bound.ruler:
                point.condition.in_bound = True

    # Calculate decan ruler
    for decan in traits.decans:
        if decan.from_degree <= point.degrees_in_sign < decan.to_degree:
            point.rulers.decan = decan.ruler

            if point.name == decan.ruler:
                point.condition.in_decan = True
