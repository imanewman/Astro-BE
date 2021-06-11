from astro.chart.relationship.sign_aspect import calculate_sign_aspect
from astro.schema import RelationshipSchema
from astro.util import AspectType, ZodiacSign
from test.utils import create_test_points


def create_separated_points(second_sign: ZodiacSign) -> RelationshipSchema:
    """
    Creates a relationship with a sign based aspect between Aries and the given sign.

    :param second_sign: The sign of the second point
    """

    from_point, to_point = create_test_points(
        {"sign": ZodiacSign.aries},
        {"sign": second_sign},
    )
    relationship = RelationshipSchema(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspect(relationship, from_point, to_point)

    return relationship


def test_calculate_sign_based_aspects__conjunction():
    """
    Tests calculating planets with a conjunction by sign.
    """

    relationship = create_separated_points(ZodiacSign.aries)

    assert relationship.sign_aspect == AspectType.conjunction


def test_calculate_sign_based_aspects__opposition():
    """
    Tests calculating planets with a opposition by sign.
    """

    relationship = create_separated_points(ZodiacSign.libra)

    assert relationship.sign_aspect == AspectType.opposition


def test_calculate_sign_based_aspects__trine():
    """
    Tests calculating planets with a trine by sign.
    """

    for sign in [ZodiacSign.sagittarius, ZodiacSign.leo]:
        relationship = create_separated_points(sign)

        assert relationship.sign_aspect == AspectType.trine


def test_calculate_sign_based_aspects__square():
    """
    Tests calculating planets with a square by sign.
    """

    for sign in [ZodiacSign.capricorn, ZodiacSign.cancer]:
        relationship = create_separated_points(sign)

        assert relationship.sign_aspect == AspectType.square


def test_calculate_sign_based_aspects__sextile():
    """
    Tests calculating planets with a sextile by sign.
    """

    for sign in [ZodiacSign.gemini, ZodiacSign.aquarius]:
        relationship = create_separated_points(sign)

        assert relationship.sign_aspect == AspectType.sextile


def test_calculate_sign_based_aspects__aversion():
    """
    Tests calculating planets in aversion by sign.
    """

    for sign in [ZodiacSign.pisces, ZodiacSign.taurus, ZodiacSign.virgo, ZodiacSign.scorpio]:
        relationship = create_separated_points(sign)

        assert relationship.sign_aspect == AspectType.aversion
