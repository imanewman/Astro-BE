from astro.schema import PointSchema
from astro.collection.zodiac_sign_traits import zodiac_sign_traits


def calculate_divisions(point: PointSchema):
    """
    Calculates the bound and decan division rulers for the given planet.

    - Sets the point's `divisions.sign_ruler` to this point's traditional sign ruler.
    - Sets the point's `divisions.bound_ruler` to this point's bound ruler.
    - Sets the point's `divisions.decan_ruler` to this point's decan ruler.
    - Sets the point's `divisions.twelfth_part_sign` to this point's 12th part.
    - Sets the point's `divisions.degree_sign` to this point's degree's sign.

    - If the point is in its own bound, `condition.in_bound` will be set.
    - If the point is in its own decan, `condition.in_decan` will be set.

    :param point: The point to calculate the division rulers for.
    """
    traits = zodiac_sign_traits.signs[point.sign]
    point.divisions.sign_ruler = traits.domicile_traditional

    # Calculate bound ruler.
    for bound in traits.bounds:
        if point.degrees_in_sign < bound.to_degree:
            point.divisions.bound_ruler = bound.ruler

            if point.name == bound.ruler:
                point.condition.in_bound = True

            break

    # Calculate decan ruler.
    decan = traits.decans[int(point.degrees_in_sign // 10)]

    point.divisions.decan_ruler = decan.ruler

    if point.name == decan.ruler:
        point.condition.in_decan = True

    # Calculate 12th part.
    part = traits.twelfth_parts[int(point.degrees_in_sign // 2.5)]

    point.divisions.twelfth_part_sign = part.sign

    # Calculate degree sign.
    degree = traits.degrees[point.degrees_in_sign]

    point.divisions.degree_sign = degree.sign
