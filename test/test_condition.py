from astro.chart.condition import calculate_divisions, calculate_triplicity, calculate_sun_conjunctions, \
    calculate_sect_placement
from astro.util import Point, SectPlacement
from test.utils import create_test_points


def test_calculate_sect_placement__none():
    """
    Tests calculating a planets placement by sect.
    """

    moon = create_test_points({})[0]

    calculate_sect_placement(moon, True)

    assert moon.condition.sect_placement is None


def test_calculate_sect_placement__sect_light():
    """
    Tests calculating when a planet is the sect light.
    """

    moon = create_test_points({})[0]

    calculate_sect_placement(moon, False)

    assert moon.condition.sect_placement is SectPlacement.sect_light


def test_calculate_sect_placement__benefic_by_sect():
    """
    Tests calculating when a planet is the benefic by sect.
    """

    jupiter, venus = create_test_points(
        {"name": Point.jupiter},
        {"name": Point.venus},
    )

    calculate_sect_placement(jupiter, True)
    calculate_sect_placement(venus, False)

    assert jupiter.condition.sect_placement is SectPlacement.benefic_by_sect
    assert venus.condition.sect_placement is SectPlacement.benefic_by_sect


def test_calculate_sect_placement__benefic_contrary_sect():
    """
    Tests calculating when a planet is the benefic contrary to sect.
    """

    jupiter, venus = create_test_points(
        {"name": Point.jupiter},
        {"name": Point.venus},
    )

    calculate_sect_placement(jupiter, False)
    calculate_sect_placement(venus, True)

    assert jupiter.condition.sect_placement is SectPlacement.benefic_contrary_sect
    assert venus.condition.sect_placement is SectPlacement.benefic_contrary_sect


def test_calculate_sect_placement__malefic_by_sect():
    """
    Tests calculating when a planet is the malefic by sect.
    """

    saturn, mars = create_test_points(
        {"name": Point.saturn},
        {"name": Point.mars},
    )

    calculate_sect_placement(saturn, True)
    calculate_sect_placement(mars, False)

    assert saturn.condition.sect_placement is SectPlacement.malefic_by_sect
    assert mars.condition.sect_placement is SectPlacement.malefic_by_sect


def test_calculate_sect_placement__malefic_contrary_sect():
    """
    Tests calculating when a planet is the malefic contrary to sect.
    """

    saturn, mars = create_test_points(
        {"name": Point.saturn},
        {"name": Point.mars},
    )

    calculate_sect_placement(saturn, False)
    calculate_sect_placement(mars, True)

    assert saturn.condition.sect_placement is SectPlacement.malefic_contrary_sect
    assert mars.condition.sect_placement is SectPlacement.malefic_contrary_sect


def test_calculate_sun_conjunctions__none():
    """
    Tests calculating the proximity of the sun to a planet.
    """

    moon, sun = create_test_points(
        {"degrees_from_aries": 180},
        {"degrees_from_aries": 200, "name": Point.sun},
        do_init_point=True
    )

    calculate_sun_conjunctions(moon, sun)

    assert moon.condition.is_cazimi is False
    assert moon.condition.is_combust is False
    assert moon.condition.is_under_beams is False


def test_calculate_sun_conjunctions__under_beams():
    """
    Tests calculating when a planet is under the beams of the sun.
    """

    moon, sun = create_test_points(
        {"degrees_from_aries": 180},
        {"degrees_from_aries": 190, "name": Point.sun},
        do_init_point=True
    )

    calculate_sun_conjunctions(moon, sun)

    assert moon.condition.is_cazimi is False
    assert moon.condition.is_combust is False
    assert moon.condition.is_under_beams is True


def test_calculate_sun_conjunctions__combust():
    """
    Tests calculating when a planet is combust the sun.
    """

    moon, sun = create_test_points(
        {"degrees_from_aries": 180},
        {"degrees_from_aries": 185, "name": Point.sun},
        do_init_point=True
    )

    calculate_sun_conjunctions(moon, sun)

    assert moon.condition.is_cazimi is False
    assert moon.condition.is_combust is True
    assert moon.condition.is_under_beams is False


def test_calculate_sun_conjunctions__cazimi():
    """
    Tests calculating when a planet is cazimi the sun.
    """

    moon, sun = create_test_points(
        {"degrees_from_aries": 180},
        {"degrees_from_aries": 180.1, "name": Point.sun},
        do_init_point=True
    )

    calculate_sun_conjunctions(moon, sun)

    assert moon.condition.is_cazimi is True
    assert moon.condition.is_combust is False
    assert moon.condition.is_under_beams is False


def test_calculate_triplicity_day():
    """
    Tests calculating the triplicity rulers during the day of a point.
    """

    moon = create_test_points({"degrees_from_aries": 180}, do_init_point=True)[0]

    calculate_triplicity(moon, True)

    assert moon.condition.in_triplicity is False
    assert moon.rulers.triplicity == (Point.saturn, Point.mercury, Point.jupiter)


def test_calculate_triplicity_night():
    """
    Tests calculating the triplicity rulers during the night of a point.
    """

    moon = create_test_points({"degrees_from_aries": 180}, do_init_point=True)[0]

    calculate_triplicity(moon, False)

    assert moon.condition.in_triplicity is False
    assert moon.rulers.triplicity == (Point.mercury, Point.saturn, Point.jupiter)


def test_calculate_triplicity_ruler():
    """
    Tests calculating whether a point is in the triplicity rulers.
    """

    moon = create_test_points({"degrees_from_aries": 150}, do_init_point=True)[0]

    calculate_triplicity(moon, True)

    assert moon.condition.in_triplicity is True


def test_calculate_divisions__beginning():
    """
    Tests calculating the divisions of a sign at the initial degree.
    """

    point = create_test_points({"degrees_from_aries": 180}, do_init_point=True)[0]

    calculate_divisions(point)

    assert point.rulers.sign == Point.venus
    assert point.rulers.bound == Point.saturn
    assert point.rulers.decan == Point.moon


def test_calculate_divisions__middle():
    """
    Tests calculating the divisions of a sign at the middle degree.
    """

    point = create_test_points({"degrees_from_aries": 195}, do_init_point=True)[0]

    calculate_divisions(point)

    assert point.rulers.sign == Point.venus
    assert point.rulers.bound == Point.jupiter
    assert point.rulers.decan == Point.saturn


def test_calculate_divisions__end():
    """
    Tests calculating the divisions of a sign at the end degree.
    """

    point = create_test_points({"degrees_from_aries": 209}, do_init_point=True)[0]

    calculate_divisions(point)

    assert point.rulers.sign == Point.venus
    assert point.rulers.bound == Point.mars
    assert point.rulers.decan == Point.jupiter


def test_calculate_divisions__cusp():
    """
    Tests calculating the divisions of a sign at the division cusps.
    """

    bound_point, decan_point = create_test_points(
        {"degrees_from_aries": 208},
        {"degrees_from_aries": 200},
        do_init_point=True
    )

    calculate_divisions(bound_point)
    calculate_divisions(decan_point)

    assert bound_point.rulers.bound == Point.mars
    assert decan_point.rulers.decan == Point.jupiter


def test_calculate_divisions__rulers():
    """
    Tests calculating when a planet is ruling its own division of a sign.
    """

    moon, mercury = create_test_points(
        {"degrees_from_aries": 185},
        {"degrees_from_aries": 190},
        do_init_point=True
    )

    calculate_divisions(moon)
    calculate_divisions(mercury)

    assert moon.condition.in_decan is True
    assert mercury.condition.in_bound is True
