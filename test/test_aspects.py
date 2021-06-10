from astro.chart.relationships import calculate_declination_aspects, calculate_sign_aspects, calculate_degree_aspects, \
    calculate_relationships, calculate_aspect_phase
from astro.schema import PointRelationship
from astro.util import AspectType, PhaseType
from test.utils import create_test_points


def test_calculate_aspects():
    """
    Tests calculating all aspects for a set of planets.
    """

    points = create_test_points(
        {"degrees_from_aries": 0, "declination": 11, "house": 1},
        {"degrees_from_aries": 5, "declination": -11, "house": 1},
    )

    aspects = calculate_relationships(points, points, True)

    assert len(aspects) is 1
    assert aspects[0].degree_aspect == AspectType.conjunction
    assert aspects[0].sign_aspect == AspectType.conjunction
    assert aspects[0].declination_aspect == AspectType.contraparallel


def test_calculate_degree_based_aspects__none():
    """
    Tests calculating planets without any degree based aspects.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 20},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect is None
    assert relationship.degree_aspect_orb is None


def test_calculate_degree_based_aspects__conjunction():
    """
    Tests calculating planets with degree based conjunctions.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 5},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.conjunction
    assert relationship.degree_aspect_orb == -5


def test_calculate_degree_based_aspects__opposition():
    """
    Tests calculating planets with degree based opposition.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 185},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.opposition
    assert relationship.degree_aspect_orb == -5


def test_calculate_degree_based_aspects__square():
    """
    Tests calculating planets with degree based square.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 95},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.square
    assert relationship.degree_aspect_orb == -5


def test_calculate_degree_based_aspects__trine():
    """
    Tests calculating planets with degree based trine.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 125},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.trine
    assert relationship.degree_aspect_orb == -5


def test_calculate_degree_based_aspects__sextile():
    """
    Tests calculating planets with degree based sextile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 65},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.sextile
    assert relationship.degree_aspect_orb == -5


def test_calculate_degree_based_aspects__quintile():
    """
    Tests calculating planets with degree based quintile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 73},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.quintile
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__septile():
    """
    Tests calculating planets with degree based septile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 52},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.septile
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__octile():
    """
    Tests calculating planets with degree based octile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 46},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.octile
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__novile():
    """
    Tests calculating planets with degree based octile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 41},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.novile
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__semi_sextile():
    """
    Tests calculating planets with degree based semi-sextile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 31},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.semi_sextile
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__quincunx():
    """
    Tests calculating planets with degree based quincunx.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 151},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.quincunx
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__sesquiquadrate():
    """
    Tests calculating planets with degree based sesquiquadrate.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 136},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.sesquiquadrate
    assert relationship.degree_aspect_orb == -1


def test_calculate_degree_based_aspects__bi_quintile():
    """
    Tests calculating planets with degree based bi-quintile.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 143},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_degree_aspects(relationship, from_point, to_point)

    assert relationship.degree_aspect == AspectType.bi_quintile
    assert relationship.degree_aspect_orb == 1


def test_calculate_phase__slower():
    """
    Tests that the slower planet (Mercury) is used as the base for the phase.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.phase_base_point == to_point.name

def test_calculate_phase__new():
    """
    Tests calculating planets with a new phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 0
    assert relationship.phase == PhaseType.new


def test_calculate_phase__crescent():
    """
    Tests calculating planets with a crescent phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 45},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 45
    assert relationship.phase == PhaseType.crescent


def test_calculate_phase__reversed():
    """
    Tests calculating planets with a crescent phase between them,
    but with reversed degrees of separation.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 15},
        {"degrees_from_aries": 330},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 45
    assert relationship.phase == PhaseType.crescent


def test_calculate_phase__first_quarter():
    """
    Tests calculating planets with a first quarter phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 90},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 90
    assert relationship.phase == PhaseType.first_quarter


def test_calculate_phase__gibbous():
    """
    Tests calculating planets with a gibbous phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 135},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 135
    assert relationship.phase == PhaseType.gibbous


def test_calculate_phase__full():
    """
    Tests calculating planets with a full phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 180},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 180
    assert relationship.phase == PhaseType.full


def test_calculate_phase__disseminating():
    """
    Tests calculating planets with a disseminating phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 225},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 225
    assert relationship.phase == PhaseType.disseminating


def test_calculate_phase__last_quarter():
    """
    Tests calculating planets with a last quarter phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 270},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 270
    assert relationship.phase == PhaseType.last_quarter


def test_calculate_phase__balsamic():
    """
    Tests calculating planets with a balsamic phase between them.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": 315},
        {"degrees_from_aries": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    assert relationship.degrees_between == 315
    assert relationship.phase == PhaseType.balsamic


def test_calculate_sign_based_aspects__conjunction():
    """
    Tests calculating planets with a conjunction by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 1})
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspects(relationship, from_point, to_point)

    assert relationship.sign_aspect == AspectType.conjunction


def test_calculate_sign_based_aspects__opposition():
    """
    Tests calculating planets with a opposition by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 7})
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspects(relationship, from_point, to_point)

    assert relationship.sign_aspect == AspectType.opposition


def test_calculate_sign_based_aspects__trine():
    """
    Tests calculating planets with a trine by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 5})
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspects(relationship, from_point, to_point)

    assert relationship.sign_aspect == AspectType.trine


def test_calculate_sign_based_aspects__square():
    """
    Tests calculating planets with a square by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 4})
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspects(relationship, from_point, to_point)

    assert relationship.sign_aspect == AspectType.square


def test_calculate_sign_based_aspects__sextile():
    """
    Tests calculating planets with a sextile by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 3})
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspects(relationship, from_point, to_point)

    assert relationship.sign_aspect == AspectType.sextile


def test_calculate_sign_based_aspects__aversion():
    """
    Tests calculating planets in aversion by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 2})
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_sign_aspects(relationship, from_point, to_point)

    assert relationship.sign_aspect == AspectType.aversion


def test_calculate_declination_aspects__none():
    """
    Tests calculating planets without a aspect by declination.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": 0},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_declination_aspects(relationship, from_point, to_point)

    assert relationship.declination_between == 20
    assert relationship.declination_aspect is None
    assert relationship.declination_aspect_orb is None


def test_calculate_declination_aspects__parallel():
    """
    Tests calculating planets with a parallel aspect by declination.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": 19.5},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_declination_aspects(relationship, from_point, to_point)

    assert relationship.declination_between == 0.5
    assert relationship.declination_aspect == AspectType.parallel
    assert relationship.declination_aspect_orb == 0.5


def test_calculate_declination_aspects__contraparallel():
    """
    Tests calculating planets with a contraparallel a aspect by declination.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": -19.5},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_declination_aspects(relationship, from_point, to_point)

    assert relationship.declination_between == 39.5
    assert relationship.declination_aspect == AspectType.contraparallel
    assert relationship.declination_aspect_orb == 0.5


def test_calculate_declination_aspects__threshold():
    """
    Tests that points at the exact orb of separation, 1 degree by default, are still considered in aspect.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": 19},
    )
    relationship = PointRelationship(from_point=from_point.name, to_point=to_point.name)

    calculate_declination_aspects(relationship, from_point, to_point)

    assert relationship.declination_between == 1
    assert relationship.declination_aspect == AspectType.parallel
    assert relationship.declination_aspect_orb == 1


