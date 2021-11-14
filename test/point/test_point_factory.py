import pytest

from astro import create_points_with_attributes
from astro.chart import calculate_point_attributes
from astro.chart.point.point_factory import create_swe_point, create_south_node, create_angles
from astro.schema import PointSchema
from astro.util import Point, ZodiacSign
from astro.util.test_events import tim_natal


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


def test_create_angles():
    """
    Tests that the ascendant and midheaven are correctly calculated.
    """

    asc, mc, desc, ic, vertex = create_angles(tim_natal.event)

    assert int(asc.longitude) == 245
    assert int(asc.declination) == -21

    assert int(mc.longitude) == 172
    assert int(mc.declination) == 2

    assert int(desc.longitude) == 65
    assert int(desc.declination) == 21

    assert int(ic.longitude) == 352
    assert int(ic.declination) == -2

    assert int(vertex.longitude) == 109
    assert int(vertex.declination) == 21


def test_create_south_node():
    """
    Tests that the south node is properly calculated from the north node.
    """

    north_node = PointSchema(
        name=Point.north_mode,
        speed=-0.05,
        longitude=168.03,
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

    point_in_time = create_swe_point(tim_natal.event, Point.saturn)

    assert round(point_in_time.longitude, 2) == 16.79
    assert round(point_in_time.declination, 2) == pytest.approx(4.05)
    assert round(point_in_time.longitude_velocity, 3) == -0.079
