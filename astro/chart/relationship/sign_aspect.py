from astro.schema import RelationshipSchema, PointSchema
from astro.util import zodiac_sign_order, AspectType


def calculate_sign_aspect(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema
):
    """
    Calculates the sign based aspect between points.

    - Sets the relationship's `sign_aspect` attribute.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    """
    if not from_point.sign or not to_point.sign:
        return

    from_sign_index = zodiac_sign_order.index(from_point.sign)
    to_sign_index = zodiac_sign_order.index(to_point.sign)
    separation = (from_sign_index - to_sign_index) % 12

    if separation == 0:
        relationship.sign_aspect = AspectType.conjunction
    elif separation == 6:
        relationship.sign_aspect = AspectType.opposition
    elif separation in [4, 8]:
        relationship.sign_aspect = AspectType.trine
    elif separation in [3, 9]:
        relationship.sign_aspect = AspectType.square
    elif separation in [2, 10]:
        relationship.sign_aspect = AspectType.sextile
    else:
        relationship.sign_aspect = AspectType.aversion
