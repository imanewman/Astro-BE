from typing import Dict

from astro.chart.condition.sect_placement import calculate_sect_placement
from astro.schema import PointSchema
from astro.util import Point, SectPlacement
from test.utils import create_test_points


def create_point_with_sect(point_args: Dict, is_day_time: bool = True) -> PointSchema:
    """
    Creates a test point with calculated sect for the given point.

    :param point_args: The args to create the point with.
    :param is_day_time: Whether the calculations are at day time.

    :return: The created point.
    """

    point = create_test_points(point_args)[0]

    calculate_sect_placement(point, is_day_time)

    return point

def test_calculate_sect_placement__none():
    """
    Tests calculating a planets placement by sect.
    """

    moon = create_point_with_sect({})

    assert moon.condition.sect_placement is None


def test_calculate_sect_placement__sect_light():
    """
    Tests calculating when a planet is the sect light.
    """

    moon = create_point_with_sect({}, False)

    assert moon.condition.sect_placement is SectPlacement.sect_light


def test_calculate_sect_placement__benefic_by_sect():
    """
    Tests calculating when a planet is the benefic by sect.
    """

    jupiter = create_point_with_sect({"name": Point.jupiter}, True)
    venus = create_point_with_sect({"name": Point.venus}, False)

    assert jupiter.condition.sect_placement is SectPlacement.benefic_by_sect
    assert venus.condition.sect_placement is SectPlacement.benefic_by_sect


def test_calculate_sect_placement__benefic_contrary_sect():
    """
    Tests calculating when a planet is the benefic contrary to sect.
    """

    jupiter = create_point_with_sect({"name": Point.jupiter}, False)
    venus = create_point_with_sect({"name": Point.venus}, True)

    assert jupiter.condition.sect_placement is SectPlacement.benefic_contrary_sect
    assert venus.condition.sect_placement is SectPlacement.benefic_contrary_sect


def test_calculate_sect_placement__malefic_by_sect():
    """
    Tests calculating when a planet is the malefic by sect.
    """

    saturn = create_point_with_sect({"name": Point.saturn}, True)
    mars = create_point_with_sect({"name": Point.mars}, False)

    assert saturn.condition.sect_placement is SectPlacement.malefic_by_sect
    assert mars.condition.sect_placement is SectPlacement.malefic_by_sect


def test_calculate_sect_placement__malefic_contrary_sect():
    """
    Tests calculating when a planet is the malefic contrary to sect.
    """

    saturn = create_point_with_sect({"name": Point.saturn}, False)
    mars = create_point_with_sect({"name": Point.mars}, True)

    assert saturn.condition.sect_placement is SectPlacement.malefic_contrary_sect
    assert mars.condition.sect_placement is SectPlacement.malefic_contrary_sect
