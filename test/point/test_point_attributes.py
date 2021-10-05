from astro.chart import calculate_point_attributes
from astro.chart.point.point_attributes import calculate_sign, calculate_degrees_in_sign, \
    calculate_minutes_in_degree, calculate_velocity_properties
from astro.schema import PointSchema
from astro.util import Point, ZodiacSign


def test_calculate_point_attributes():
    """
    Tests that a sign is correctly calculated from the degrees from aries.
    """

    point = PointSchema(
        name=Point.mercury,
        longitude_velocity=1.73444,
        longitude=196.69
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

    point = PointSchema(
        name=Point.mercury,
        longitude_velocity=1.5,
        longitude=1
    )

    calculate_velocity_properties(point)

    assert point.is_stationary is False
    assert point.is_retrograde is False


def test_calculate_speed_properties__stationary_direct():
    """
    Tests that a planet moving stationary direct has the proper attributes.
    """

    point = PointSchema(
        name=Point.mercury,
        longitude_velocity=0.1,
        longitude=1
    )

    calculate_velocity_properties(point)

    assert point.is_stationary is True
    assert point.is_retrograde is False


def test_calculate_speed_properties__retrograde():
    """
    Tests that a planet moving retrograde has the proper attributes.
    """

    point = PointSchema(
        name=Point.mercury,
        longitude_velocity=-1.5,
        longitude=1
    )

    calculate_velocity_properties(point)

    assert point.is_stationary is False
    assert point.is_retrograde is True


def test_calculate_speed_properties__stationary_retrograde():
    """
    Tests that a planet moving stationary retrograde has the proper attributes.
    """

    point = PointSchema(
        name=Point.mercury,
        longitude_velocity=-0.1,
        longitude=1
    )

    calculate_velocity_properties(point)

    assert point.is_stationary is True
    assert point.is_retrograde is True
