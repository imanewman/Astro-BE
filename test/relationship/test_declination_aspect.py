from astro.chart.relationship.declination_aspect import calculate_declination_aspect
from astro.schema import RelationshipSchema
from astro.util import AspectType
from test.utils import create_test_points


def create_separated_points(from_declination: float, to_declination: float) -> RelationshipSchema:
    """
    Creates a relationship with a declination aspect by the given degrees of separation.

    :param from_declination: The degrees of declination of the first point.
    :param to_declination: The degrees of declination of the second point.
    """

    from_point, to_point = create_test_points(
        {"declination": from_declination},
        {"declination": to_declination},
    )
    relationship = RelationshipSchema(from_point=from_point.name, to_point=to_point.name)

    calculate_declination_aspect(relationship, from_point, to_point)

    return relationship


def test_calculate_declination_aspects__none():
    """
    Tests calculating planets without a aspect by declination.
    """

    relationship = create_separated_points(20, 0)

    assert relationship.declination_between == 20
    assert relationship.declination_aspect is None
    assert relationship.declination_aspect_orb is None


def test_calculate_declination_aspects__parallel():
    """
    Tests calculating planets with a parallel aspect by declination.
    """

    relationship = create_separated_points(20, 19.5)

    assert relationship.declination_between == 0.5
    assert relationship.declination_aspect == AspectType.parallel
    assert relationship.declination_aspect_orb == 0.5


def test_calculate_declination_aspects__parallel_reversed():
    """
    Tests calculating planets with a parallel aspect by declination.
    """

    relationship = create_separated_points(19.5, 20)

    assert relationship.declination_between == 0.5
    assert relationship.declination_aspect_orb == 0.5


def test_calculate_declination_aspects__contraparallel():
    """
    Tests calculating planets with a contraparallel a aspect by declination.
    """

    relationship = create_separated_points(20, -19.5)

    assert relationship.declination_between == 39.5
    assert relationship.declination_aspect == AspectType.contraparallel
    assert relationship.declination_aspect_orb == 0.5


def test_calculate_declination_aspects__contraparallel_reversed():
    """
    Tests calculating planets with a contraparallel a aspect by declination.
    """

    relationship = create_separated_points(-19.5, 20)

    assert relationship.declination_between == 39.5
    assert relationship.declination_aspect_orb == 0.5


def test_calculate_declination_aspects__threshold():
    """
    Tests that points at the exact orb of separation, 1 degree by default, are still considered in aspect.
    """

    relationship = create_separated_points(20, 19)

    assert relationship.declination_between == 1
    assert relationship.declination_aspect == AspectType.parallel
    assert relationship.declination_aspect_orb == 1
