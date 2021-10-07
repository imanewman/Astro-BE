from astro.chart.point import create_points_with_attributes
from astro.chart import calculate_whole_sign_house_cusps, calculate_whole_sign_house_of_point, \
    calculate_traditional_house_rulers, calculate_whole_sign_houses, calculate_secondary_houses, \
    calculate_secondary_house_cusps, calculate_secondary_house_of_point
from astro.util import ZodiacSign, Point, HouseSystem
from astro.util.tim import tim_natal


def test_calculate_whole_sign_houses():
    """
    Tests that all the information about house placements is added.
    """

    points = create_points_with_attributes(tim_natal)
    houses_whole_sign = calculate_whole_sign_houses(points)

    assert houses_whole_sign[0].number is 1
    assert houses_whole_sign[0].sign == ZodiacSign.sagittarius
    assert houses_whole_sign[0].points == [Point.ascendant, Point.venus, Point.mars, Point.pluto]

    assert points[Point.venus].houses_whole_sign.house is 1
    assert points[Point.venus].houses_whole_sign.ruled_houses == [6, 11]


def test_calculate_whole_sign_house_cusps():
    """
    Tests that the houses are properly calculated from the ascendant.
    """

    asc = create_points_with_attributes(tim_natal)[Point.ascendant]
    house_placements, houses = calculate_whole_sign_house_cusps(asc)

    assert houses[0] == ZodiacSign.sagittarius
    assert houses[11] == ZodiacSign.scorpio

    assert house_placements[0].number is 1
    assert house_placements[0].sign == ZodiacSign.sagittarius
    assert house_placements[11].number is 12
    assert house_placements[11].sign == ZodiacSign.scorpio


def test_calculate_whole_sign_house_of_point():
    """
    Tests that the houses a planet falls in are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)
    asc = points[Point.ascendant]
    mercury = points[Point.mercury]
    house_placements = calculate_whole_sign_house_cusps(asc)[0]

    calculate_whole_sign_house_of_point(mercury, house_placements)

    assert mercury.houses_whole_sign.house is 11
    assert house_placements[10].points == [Point.mercury]


def test_calculate_whole_sign_house_rulers():
    """
    Tests that the houses each planet rules are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)
    asc = points[Point.ascendant]
    mercury = points[Point.mercury]
    jupiter = points[Point.jupiter]
    houses = calculate_whole_sign_house_cusps(asc)[0]

    calculate_traditional_house_rulers(points, houses, True)

    assert mercury.houses_whole_sign.ruled_houses == [7, 10]
    assert jupiter.houses_whole_sign.ruled_houses == [1, 4]


def test_calculate_secondary_houses():
    """
    Tests that all the information about house placements is added.
    """

    points = create_points_with_attributes(tim_natal)
    houses_secondary = calculate_secondary_houses(points, tim_natal.event, HouseSystem.porphyry)

    assert houses_secondary[0].number is 1
    assert houses_secondary[0].sign == ZodiacSign.sagittarius
    assert houses_secondary[0].points == [Point.ascendant, Point.mars]

    assert points[Point.venus].houses_secondary.house is 12
    assert points[Point.venus].houses_secondary.ruled_houses == [6, 11]


def test_calculate_secondary_house_cusps():
    """
    Tests that the houses are properly calculated from the ascendant.
    """

    house_placements = calculate_secondary_house_cusps(tim_natal.event, HouseSystem.porphyry)

    assert house_placements[0].number is 1
    assert house_placements[0].sign == ZodiacSign.sagittarius
    assert house_placements[11].number is 12
    assert house_placements[11].sign == ZodiacSign.scorpio


def test_calculate_secondary_house_of_point__normal():
    """
    Tests that the houses a planet falls in are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)
    venus = points[Point.venus]
    house_placements = calculate_secondary_house_cusps(tim_natal.event, HouseSystem.porphyry)

    calculate_secondary_house_of_point(venus, house_placements)

    assert venus.houses_secondary.house is 12
    assert house_placements[11].points == [Point.venus]


def test_calculate_secondary_house_of_point__wrapped():
    """
    Tests that the houses a planet falls in are properly calculated
    when the following house cusp wraps past 0 degrees longitude.
    """

    points = create_points_with_attributes(tim_natal)
    inner_heaven = points[Point.inner_heaven]
    house_placements = calculate_secondary_house_cusps(tim_natal.event, HouseSystem.porphyry)

    calculate_secondary_house_of_point(inner_heaven, house_placements)

    assert inner_heaven.houses_secondary.house is 4
    assert house_placements[3].points == [Point.inner_heaven]


def test_calculate_secondary_house_rulers():
    """
    Tests that the houses each planet rules are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)
    mercury = points[Point.mercury]
    jupiter = points[Point.jupiter]
    house_placements = calculate_secondary_house_cusps(tim_natal.event, HouseSystem.porphyry)

    calculate_traditional_house_rulers(points, house_placements, False)

    assert mercury.houses_secondary.ruled_houses == [7, 10]
    assert jupiter.houses_secondary.ruled_houses == [1, 4]
