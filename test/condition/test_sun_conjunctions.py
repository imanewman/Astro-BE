from astro.chart.condition.sun_conjunctions import calculate_sun_conjunctions
from astro.schema import PointSchema
from astro.util import Point
from test.utils import create_test_points


def create_sun_conjunction(degrees_between: float) -> PointSchema:
    """
    Creates a sun and moon and calculates sun conjunction properties.

    :param degrees_between: The degrees between the sun and moon.

    :return: The moon.
    """

    moon, sun = create_test_points(
        {"longitude": 0},
        {"longitude": degrees_between, "name": Point.sun},
        do_init_point=True
    )

    calculate_sun_conjunctions(moon, sun)

    return moon


def test_calculate_sun_conjunctions__none():
    """
    Tests calculating the proximity of the sun to a planet.
    """

    moon = create_sun_conjunction(20)

    assert moon.condition.is_cazimi is False
    assert moon.condition.is_combust is False
    assert moon.condition.is_under_beams is False


def test_calculate_sun_conjunctions__under_beams():
    """
    Tests calculating when a planet is under the beams of the sun.
    """

    moon = create_sun_conjunction(10)

    assert moon.condition.is_cazimi is False
    assert moon.condition.is_combust is False
    assert moon.condition.is_under_beams is True


def test_calculate_sun_conjunctions__combust():
    """
    Tests calculating when a planet is combust the sun.
    """

    moon = create_sun_conjunction(5)

    assert moon.condition.is_cazimi is False
    assert moon.condition.is_combust is True
    assert moon.condition.is_under_beams is False


def test_calculate_sun_conjunctions__cazimi():
    """
    Tests calculating when a planet is cazimi the sun.
    """

    moon = create_sun_conjunction(0.1)

    assert moon.condition.is_cazimi is True
    assert moon.condition.is_combust is False
    assert moon.condition.is_under_beams is False
