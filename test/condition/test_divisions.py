from astro.chart.condition.divisions import calculate_divisions
from astro.util import Point
from test.utils import create_test_points


def test_calculate_divisions__beginning():
    """
    Tests calculating the divisions of a sign at the initial degree.
    """

    point = create_test_points({"longitude": 180}, do_init_point=True)[0]

    calculate_divisions(point)

    assert point.rulers.sign == Point.venus
    assert point.rulers.bound == Point.saturn
    assert point.rulers.decan == Point.moon


def test_calculate_divisions__middle():
    """
    Tests calculating the divisions of a sign at the middle degree.
    """

    point = create_test_points({"longitude": 195}, do_init_point=True)[0]

    calculate_divisions(point)

    assert point.rulers.sign == Point.venus
    assert point.rulers.bound == Point.jupiter
    assert point.rulers.decan == Point.saturn


def test_calculate_divisions__end():
    """
    Tests calculating the divisions of a sign at the end degree.
    """

    point = create_test_points({"longitude": 209}, do_init_point=True)[0]

    calculate_divisions(point)

    assert point.rulers.sign == Point.venus
    assert point.rulers.bound == Point.mars
    assert point.rulers.decan == Point.jupiter


def test_calculate_divisions__cusp():
    """
    Tests calculating the divisions of a sign at the division cusps.
    """

    bound_point, decan_point = create_test_points(
        {"longitude": 208},
        {"longitude": 200},
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
        {"longitude": 185},
        {"longitude": 190},
        do_init_point=True
    )

    calculate_divisions(moon)
    calculate_divisions(mercury)

    assert moon.condition.in_decan is True
    assert mercury.condition.in_bound is True
