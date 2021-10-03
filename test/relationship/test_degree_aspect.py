from astro.chart import calculate_degree_aspect
from astro.schema import RelationshipSchema
from astro.util import AspectType
from test.utils import create_test_points


def create_separated_points(degrees_of_separation: int) -> RelationshipSchema:
    """
    Creates a relationship with a degree aspect by the given degrees of separation.

    :param degrees_of_separation: The degrees of separation between points.

    :return: The created relationship.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": degrees_of_separation % 360},
    )
    relationship = RelationshipSchema(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspect(relationship, from_point, to_point)

    return relationship


def test_calculate_degree_based_aspects__none():
    """
    Tests calculating planets without any degree based aspects.
    """

    relationship = create_separated_points(20)

    assert relationship.arc_between == 20
    assert relationship.degree_aspect is None
    assert relationship.degree_aspect_angle is None
    assert relationship.degree_aspect_orb is None


def test_calculate_degree_based_aspects__degrees_polarity():
    """
    Tests that the polarity of degrees between points is always correct.
    """

    assert create_separated_points(20).arc_between == 20
    assert create_separated_points(-20).arc_between == 20


def test_calculate_degree_based_aspects__conjunction():
    """
    Tests calculating planets with degree based conjunctions.
    """

    relationship = create_separated_points(5)

    assert relationship.arc_between == 5
    assert relationship.degree_aspect == AspectType.conjunction
    assert relationship.degree_aspect_angle == 0
    assert relationship.degree_aspect_orb == 5


def test_calculate_degree_based_aspects__exists_polarity():
    """
    Tests that the polarity of aspect orb between points is always correct,
    from the first to the second point.
    """

    assert create_separated_points(5).degree_aspect_orb == 5
    assert create_separated_points(-5).degree_aspect_orb == -5


def test_calculate_degree_based_aspects__opposition():
    """
    Tests calculating planets with degree based opposition.
    """

    relationship = create_separated_points(185)

    assert relationship.degree_aspect == AspectType.opposition
    assert relationship.degree_aspect_orb == 5


def test_calculate_degree_based_aspects__square():
    """
    Tests calculating planets with degree based square.
    """

    relationship = create_separated_points(95)

    assert relationship.degree_aspect == AspectType.square
    assert relationship.degree_aspect_orb == 5


def test_calculate_degree_based_aspects__trine():
    """
    Tests calculating planets with degree based trine.
    """

    relationship = create_separated_points(125)

    assert relationship.degree_aspect == AspectType.trine
    assert relationship.degree_aspect_orb == 5


def test_calculate_degree_based_aspects__sextile():
    """
    Tests calculating planets with degree based sextile.
    """

    relationship = create_separated_points(65)

    assert relationship.degree_aspect == AspectType.sextile
    assert relationship.degree_aspect_orb == 5


def test_calculate_degree_based_aspects__quintile():
    """
    Tests calculating planets with degree based quintile.
    """

    relationship = create_separated_points(73)

    assert relationship.degree_aspect == AspectType.quintile
    assert relationship.degree_aspect_orb == 1


def test_calculate_degree_based_aspects__septile():
    """
    Tests calculating planets with degree based septile.
    """

    relationship = create_separated_points(52)

    assert relationship.degree_aspect == AspectType.septile
    assert relationship.degree_aspect_orb == 1


def test_calculate_degree_based_aspects__octile():
    """
    Tests calculating planets with degree based octile.
    """

    relationship = create_separated_points(46)

    assert relationship.degree_aspect == AspectType.octile
    assert relationship.degree_aspect_orb == 1


def test_calculate_degree_based_aspects__novile():
    """
    Tests calculating planets with degree based octile.
    """

    relationship = create_separated_points(39)

    assert relationship.degree_aspect == AspectType.novile
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__semi_sextile():
    """
    Tests calculating planets with degree based semi-sextile.
    """

    relationship = create_separated_points(31)

    assert relationship.degree_aspect == AspectType.semi_sextile
    assert relationship.degree_aspect_orb == 1


def test_calculate_degree_based_aspects__quincunx():
    """
    Tests calculating planets with degree based quincunx.
    """

    relationship = create_separated_points(151)

    assert relationship.degree_aspect == AspectType.quincunx
    assert relationship.degree_aspect_orb == 1


def test_calculate_degree_based_aspects__sesquiquadrate():
    """
    Tests calculating planets with degree based sesquiquadrate.
    """

    relationship = create_separated_points(136)

    assert relationship.degree_aspect == AspectType.sesquiquadrate
    assert relationship.degree_aspect_orb == 1


def test_calculate_degree_based_aspects__bi_quintile():
    """
    Tests calculating planets with degree based bi-quintile.
    """

    relationship = create_separated_points(143)

    assert relationship.degree_aspect == AspectType.bi_quintile
    assert relationship.degree_aspect_orb == -1
