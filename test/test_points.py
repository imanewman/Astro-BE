import pytest

from astro import create_points_with_attributes
from astro.chart import calculate_point_attributes
from astro.chart.point.point_factory import create_swe_point, create_asc_mc, create_south_node
from astro.chart.point.point_attributes import calculate_sign, calculate_degrees_in_sign, \
    calculate_minutes_in_degree, calculate_speed_properties
from astro.schema import PointInTime
from astro.util import tim_natal, Point, ZodiacSign


def test_create_all_points():
    """
    Tests that all points are calculated, by checking the high level of the signs of each.
    """

    points = create_points_with_attributes(tim_natal)

    assert points[Point.ascendant].sign is ZodiacSign.sagittarius
    assert points[Point.midheaven].sign is ZodiacSign.virgo
    assert points[Point.moon].sign is ZodiacSign.aquarius
    assert points[Point.mercury].sign is ZodiacSign.libra
    assert points[Point.venus].sign is ZodiacSign.sagittarius
    assert points[Point.sun].sign is ZodiacSign.libra
    assert points[Point.mars].sign is ZodiacSign.sagittarius
    assert points[Point.jupiter].sign is ZodiacSign.aquarius
    assert points[Point.saturn].sign is ZodiacSign.aries
    assert points[Point.uranus].sign is ZodiacSign.aquarius
    assert points[Point.neptune].sign is ZodiacSign.capricorn
    assert points[Point.pluto].sign is ZodiacSign.sagittarius
    assert points[Point.north_mode].sign is ZodiacSign.virgo
    assert points[Point.south_node].sign is ZodiacSign.pisces


def test_create_asc_mc():
    """
    Tests that the ascendant and midheaven are correctly calculated.
    """

    asc, mc = create_asc_mc(tim_natal)

    calculate_point_attributes(asc)
    calculate_point_attributes(mc)

    assert asc.sign is ZodiacSign.sagittarius
    assert asc.degrees_in_sign is 5

    assert mc.sign is ZodiacSign.virgo
    assert mc.degrees_in_sign is 22


def test_create_south_node():
    """
    Tests that the south node is properly calculated from the north node.
    """

    north_node = PointInTime(
        name=Point.north_mode,
        speed=-0.05,
        degrees_from_aries=168.03,
        declination=4.73,
    )

    south_node = create_south_node(north_node)

    calculate_point_attributes(north_node)
    calculate_point_attributes(south_node)

    assert north_node.sign is ZodiacSign.virgo
    assert north_node.degrees_in_sign is 18
    assert north_node.declination == 4.73

    assert south_node.sign is ZodiacSign.pisces
    assert south_node.degrees_in_sign is 18
    assert south_node.declination == -4.73


def test_create_point():
    """
    Tests that a points location and speed is correctly calculated.
    """

    point_in_time = create_swe_point(tim_natal, Point.saturn)

    assert point_in_time.degrees_from_aries == pytest.approx(16.79)
    assert point_in_time.declination == pytest.approx(4.05)
    assert point_in_time.speed == pytest.approx(-0.079, abs=1e-3)


def test_calculate_point_attributes():
    """
    Tests that a sign is correctly calculated from the degrees from aries.
    """

    point = PointInTime(
        name=Point.mercury,
        speed=1.73444,
        degrees_from_aries=196.69
    )

    calculate_point_attributes(point)

    assert point.sign is ZodiacSign.libra
    assert point.degrees_in_sign is 16
    assert point.minutes_in_degree is 41
    assert point.is_stationary is False
    assert point.is_retrograde is False


def test_calculate_sign():
    """
    Tests that a sign is correctly calculated from the degrees from aries.
    """

    assert calculate_sign(180) is ZodiacSign.libra
    assert calculate_sign(179.99) is ZodiacSign.virgo


def test_calculate_degrees_in_sign():
    """
    Tests that the number of degrees in a sign is correctly calculated.
    """

    assert calculate_degrees_in_sign(181.23) is 1


def test_calculate_minutes_in_degree():
    """
    Tests that the number of minutes in a degree is correctly calculated.
    """

    assert calculate_minutes_in_degree(181.25) is 15


def test_calculate_speed_properties__direct():
    """
    Tests that a planet moving direct has the proper attributes.
    """

    point = PointInTime(
        name=Point.mercury,
        speed=1.5,
        degrees_from_aries=1
    )

    calculate_speed_properties(point)

    assert point.is_stationary is False
    assert point.is_retrograde is False


def test_calculate_speed_properties__stationary_direct():
    """
    Tests that a planet moving stationary direct has the proper attributes.
    """

    point = PointInTime(
        name=Point.mercury,
        speed=0.1,
        degrees_from_aries=1
    )

    calculate_speed_properties(point)

    assert point.is_stationary is True
    assert point.is_retrograde is False


def test_calculate_speed_properties__retrograde():
    """
    Tests that a planet moving retrograde has the proper attributes.
    """

    point = PointInTime(
        name=Point.mercury,
        speed=-1.5,
        degrees_from_aries=1
    )

    calculate_speed_properties(point)

    assert point.is_stationary is False
    assert point.is_retrograde is True


def test_calculate_speed_properties__stationary_retrograde():
    """
    Tests that a planet moving stationary retrograde has the proper attributes.
    """

    point = PointInTime(
        name=Point.mercury,
        speed=-0.1,
        degrees_from_aries=1
    )

    calculate_speed_properties(point)

    assert point.is_stationary is True
    assert point.is_retrograde is True
