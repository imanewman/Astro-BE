from astro.chart.point import create_points_with_attributes
from astro.chart import calculate_whole_sign_houses, calculate_house_of_point, calculate_traditional_house_rulers, \
    calculate_houses
from astro.util import tim_natal, ZodiacSign, Point


def test_calculate_houses():
    """
    Tests that all the information about house placements is added.
    """

    points = create_points_with_attributes(tim_natal)
    house_placements = calculate_houses(points)

    assert house_placements[0].number is 1
    assert house_placements[0].sign == ZodiacSign.sagittarius
    assert house_placements[0].points == [Point.ascendant, Point.venus, Point.mars, Point.pluto]

    assert points[Point.venus].house is 1
    assert points[Point.venus].ruled_houses == [6, 11]


def test_calculate_whole_sign_houses():
    """
    Tests that the houses are properly calculated from the ascendant.
    """

    asc = create_points_with_attributes(tim_natal)[Point.ascendant]
    house_placements, houses = calculate_whole_sign_houses(asc)

    assert houses[0] == ZodiacSign.sagittarius
    assert houses[11] == ZodiacSign.scorpio

    assert house_placements[0].number is 1
    assert house_placements[0].sign == ZodiacSign.sagittarius
    assert house_placements[11].number is 12
    assert house_placements[11].sign == ZodiacSign.scorpio


def test_calculate_house_of_point():
    """
    Tests that the houses a planet falls in are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)
    asc = points[Point.ascendant]
    mercury = points[Point.mercury]
    house_placements = calculate_whole_sign_houses(asc)[0]

    calculate_house_of_point(mercury, house_placements)

    assert mercury.house is 11
    assert house_placements[10].points == [Point.mercury]


def test_calculate_traditional_house_rulers():
    """
    Tests that the houses each planet rules are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)
    asc = points[Point.ascendant]
    mercury = points[Point.mercury]
    jupiter = points[Point.jupiter]
    houses = calculate_whole_sign_houses(asc)[1]

    calculate_traditional_house_rulers(points, houses)

    assert mercury.ruled_houses == [7, 10]
    assert jupiter.ruled_houses == [1, 4]
