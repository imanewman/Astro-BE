from typing import Dict

from astro.chart.condition.primary_dignities import calculate_primary_dignities
from astro.schema import PointSchema
from astro.util import ZodiacSign
from test.utils import create_test_points


def create_point_with_dignities(point_args: Dict) -> PointSchema:
    """
    Creates a test point with calculated dignities for the given point.

    :param point_args: The args to create the point with.

    :return: The created point.
    """

    point = create_test_points(point_args)[0]

    calculate_primary_dignities(point)

    return point


def test_calculate_primary_dignities__none():
    """
    Tests calculating when a planet is in joy, domicile, exaltation, detriment, or fall.
    """

    moon = create_point_with_dignities({"house": 1})

    assert moon.condition.in_joy is False
    assert moon.condition.in_domicile is False
    assert moon.condition.in_exaltation is False
    assert moon.condition.in_detriment is False
    assert moon.condition.in_fall is False


def test_calculate_primary_dignities__joy():
    """
    Tests calculating when a planet is in joy.
    """

    moon = create_point_with_dignities({
        "houses_whole_sign": {"house": 3}
    })

    assert moon.condition.in_joy is True


def test_calculate_primary_dignities__domicile():
    """
    Tests calculating when a planet is in domicile.
    """

    moon = create_point_with_dignities({"sign": ZodiacSign.cancer})

    assert moon.condition.in_domicile is True


def test_calculate_primary_dignities__exaltation():
    """
    Tests calculating when a planet is in exaltation.
    """

    moon = create_point_with_dignities({"sign": ZodiacSign.taurus})

    assert moon.condition.in_exaltation is True


def test_calculate_primary_dignities__detriment():
    """
    Tests calculating when a planet is in detriment.
    """

    moon = create_point_with_dignities({"sign": ZodiacSign.capricorn})

    assert moon.condition.in_detriment is True


def test_calculate_primary_dignities__fall():
    """
    Tests calculating when a planet is in fall.
    """

    moon = create_point_with_dignities({"sign": ZodiacSign.scorpio})

    assert moon.condition.in_fall is True
