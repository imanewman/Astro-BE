from astro.util import AspectType
from test.utils import create_test_points


def test_calculate_aspects():
    """
    Tests calculating all aspects for a set of planets.
    """

    points = create_test_points(
        {"degrees_from_aries": 0, "declination": 11, "house": 1},
        {"degrees_from_aries": 5, "declination": -11, "house": 1},
    )

    aspects = calculate_aspects(points, points, True)

    assert len(aspects.by_degree) is 1
    assert aspects.by_degree[0].type == AspectType.conjunction
    assert len(aspects.by_sign) is 1
    assert aspects.by_sign[0].type == AspectType.conjunction
    assert len(aspects.by_sign) is 1
    assert aspects.by_declination[0].type == AspectType.contraparallel


def test_calculate_degree_based_aspects__none():
    """
    Tests calculating planets without any degree based aspects.
    """

    from_point, to_point = create_test_points({"degrees_from_aries": 0}, {"degrees_from_aries": 20})
    aspects = calculate_degree_based_aspects([from_point], [to_point])

    assert len(aspects) is 0


def test_calculate_degree_based_aspects__conjunction():
    """
    Tests calculating planets with degree based conjunctions.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 5},
        {"degrees_from_aries": 355}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.conjunction
    assert aspects[0].orb == -5
    assert aspects[1].type == AspectType.conjunction
    assert aspects[1].orb == 5


def test_calculate_degree_based_aspects__opposition():
    """
    Tests calculating planets with degree based opposition.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 185},
        {"degrees_from_aries": 175}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.opposition
    assert aspects[0].orb == -5
    assert aspects[1].type == AspectType.opposition
    assert aspects[1].orb == 5


def test_calculate_degree_based_aspects__square():
    """
    Tests calculating planets with degree based square.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 95},
        {"degrees_from_aries": 265}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.square
    assert aspects[0].orb == -5
    assert aspects[1].type == AspectType.square
    assert aspects[1].orb == 5


def test_calculate_degree_based_aspects__trine():
    """
    Tests calculating planets with degree based trine.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 125},
        {"degrees_from_aries": 235}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.trine
    assert aspects[0].orb == -5
    assert aspects[1].type == AspectType.trine
    assert aspects[1].orb == 5


def test_calculate_degree_based_aspects__sextile():
    """
    Tests calculating planets with degree based sextile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 65},
        {"degrees_from_aries": 295}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.sextile
    assert aspects[0].orb == -5
    assert aspects[1].type == AspectType.sextile
    assert aspects[1].orb == 5


def test_calculate_degree_based_aspects__quintile():
    """
    Tests calculating planets with degree based quintile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 73},
        {"degrees_from_aries": 287}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.quintile
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.quintile
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__septile():
    """
    Tests calculating planets with degree based septile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 52},
        {"degrees_from_aries": 308}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.septile
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.septile
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__octile():
    """
    Tests calculating planets with degree based octile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 46},
        {"degrees_from_aries": 314}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.octile
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.octile
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__novile():
    """
    Tests calculating planets with degree based octile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 41},
        {"degrees_from_aries": 319}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.novile
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.novile
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__semi_sextile():
    """
    Tests calculating planets with degree based semi-sextile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 31},
        {"degrees_from_aries": 329}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.semi_sextile
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.semi_sextile
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__quincunx():
    """
    Tests calculating planets with degree based quincunx.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 151},
        {"degrees_from_aries": 209}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.quincunx
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.quincunx
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__sesquiquadrate():
    """
    Tests calculating planets with degree based sesquiquadrate.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 136},
        {"degrees_from_aries": 224}
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.sesquiquadrate
    assert aspects[0].orb == -1
    assert aspects[1].type == AspectType.sesquiquadrate
    assert aspects[1].orb == 1


def test_calculate_degree_based_aspects__bi_quintile():
    """
    Tests calculating planets with degree based bi-quintile.
    """

    points = create_test_points(
        {"degrees_from_aries": 0},
        {"degrees_from_aries": 143},
    )

    aspects = calculate_degree_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.bi_quintile
    assert aspects[0].orb == 1


def test_calculate_sign_based_aspects__natal():
    """
    Tests calculating planets with an aspect by sign in natal chart.
    Asserts that there arent duplicate aspects between a point and itself
    """

    natal_points = create_test_points({"house": 1}, {"house": 7})
    aspects = calculate_sign_based_aspects(natal_points, natal_points, True)

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.opposition


def test_calculate_sign_based_aspects__conjunction():
    """
    Tests calculating planets with a conjunction by sign.
    """

    from_point, to_point = create_test_points({"house": 1}, {"house": 1})
    aspects = calculate_sign_based_aspects([from_point], [to_point])

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.conjunction


def test_calculate_sign_based_aspects__opposition():
    """
        Tests calculating planets with a opposition by sign.
        """

    from_point, to_point = create_test_points({"house": 1}, {"house": 7})
    aspects = calculate_sign_based_aspects([from_point], [to_point])

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.opposition


def test_calculate_sign_based_aspects__trine():
    """
    Tests calculating planets with a trine by sign.
    """

    points = create_test_points({"house": 1}, {"house": 5}, {"house": 9})
    aspects = calculate_sign_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.trine
    assert aspects[1].type == AspectType.trine


def test_calculate_sign_based_aspects__square():
    """
    Tests calculating planets with a square by sign.
    """

    points = create_test_points({"house": 1}, {"house": 4}, {"house": 10})
    aspects = calculate_sign_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.square
    assert aspects[1].type == AspectType.square


def test_calculate_sign_based_aspects__sextile():
    """
    Tests calculating planets with a sextile by sign.
    """

    points = create_test_points({"house": 1}, {"house": 3}, {"house": 11})
    aspects = calculate_sign_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.sextile
    assert aspects[1].type == AspectType.sextile


def test_calculate_sign_based_aspects__aversion():
    """
    Tests calculating planets with a sextile by sign.
    """

    points = create_test_points({"house": 1}, {"house": 2}, {"house": 12})
    aspects = calculate_sign_based_aspects(points[0:1], points[1:])

    assert len(aspects) is 2
    assert aspects[0].type == AspectType.aversion
    assert aspects[1].type == AspectType.aversion


def test_calculate_declination_aspects__none():
    """
    Tests calculating planets without a aspect by declination.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": 0},
    )

    aspects = calculate_declination_aspects([from_point], [to_point])

    assert len(aspects) is 0


def test_calculate_declination_aspects__natal():
    """
    Tests calculating planets with an aspect by declination in natal chart.
    Asserts that there arent duplicate aspects between a point and itself.
    """

    points = create_test_points(
        {"declination": 0},
        {"declination": 0},
    )

    aspects = calculate_declination_aspects(points, points, True)

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.parallel


def test_calculate_declination_aspects__parallel():
    """
    Tests calculating planets with a parallel aspect by declination.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": 19.5},
    )

    aspects = calculate_declination_aspects([from_point], [to_point])

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.parallel
    assert aspects[0].orb == 0.5


def test_calculate_declination_aspects__contraparallel():
    """
    Tests calculating planets with a contraparallel a aspect by declination.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": -19.5},
    )

    aspects = calculate_declination_aspects([from_point], [to_point])

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.contraparallel
    assert aspects[0].orb == 0.5


def test_calculate_declination_aspects__threshold():
    """
    Tests that points at the exact orb of separation, 1 degree by default, are still considered in aspect.
    """

    from_point, to_point = create_test_points(
        {"declination": 20},
        {"declination": 19},
    )

    aspects = calculate_declination_aspects([from_point], [to_point])

    assert len(aspects) is 1
    assert aspects[0].type == AspectType.parallel
    assert aspects[0].orb == 1


