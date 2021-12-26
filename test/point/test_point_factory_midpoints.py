from typing import Optional, Dict

from astro.chart.point.midpoint_factory import create_midpoint
from astro.schema import PointSchema, MidpointSettingsSchema
from astro.util import Point


def create_test_midpoint(
        from_props: Dict,
        to_props: Dict
) -> Optional[PointSchema]:
    return create_midpoint(
        {
            Point.moon: PointSchema(
                name=Point.moon,
                points=[Point.moon],
                **from_props
            ),
            Point.sun: PointSchema(
                name=Point.sun,
                points=[Point.sun],
                **to_props
            ),
        },
        MidpointSettingsSchema(
            from_point=Point.moon,
            to_point=Point.sun,
        )
    )


def test_create_no_midpoint():
    """
    Tests creating a midpoint when one of the points is missing.
    """
    midpoint = MidpointSettingsSchema(
        from_point=Point.moon,
        to_point=Point.sun,
    )

    assert create_midpoint({
        Point.moon: PointSchema(
            name=Point.moon,
            points=[Point.moon],
            longitude=0
        )
    }, midpoint) is None
    assert create_midpoint({
        Point.sun: PointSchema(
            name=Point.sun,
            points=[Point.sun],
            longitude=0
        )
    }, midpoint) is None


def test_create_longitude_midpoint__acute():
    """
    Tests creating a midpoint in longitude.
    """
    midpoint = create_test_midpoint({"longitude": 10}, {"longitude": 20})

    assert midpoint.longitude == 15


def test_create_longitude_midpoint__obtuse():
    """
    Tests creating a midpoint in longitude in reversed order.
    """
    midpoint = create_test_midpoint({"longitude": 20}, {"longitude": 10})

    assert midpoint.longitude == 15


def test_create_longitude_midpoint__overflow():
    """
    Tests creating a midpoint that wraps back through 0 degrees.
    """
    midpoint = create_test_midpoint({"longitude": 350}, {"longitude": 20})

    assert midpoint.longitude == 5


def test_create_declination_midpoint__none():
    """
    Tests creating a midpoint in declination with a missing value.
    """
    midpoint = create_test_midpoint({
        "longitude": 0},
        {"longitude": 0, "declination": 20}
    )

    assert midpoint.declination is None


def test_create_declination_midpoint__positive():
    """
    Tests creating a midpoint in positive declination.
    """
    midpoint = create_test_midpoint({
        "longitude": 0, "declination": 10},
        {"longitude": 0, "declination": 20}
    )

    assert midpoint.declination == 15


def test_create_declination_midpoint__negative():
    """
    Tests creating a midpoint in negative declination.
    """
    midpoint = create_test_midpoint({
        "longitude": 0, "declination": -10},
        {"longitude": 0, "declination": -20}
    )

    assert midpoint.declination == -15


def test_create_declination_midpoint__mixed():
    """
    Tests creating a midpoint in mixed sign declination.
    """
    midpoint = create_test_midpoint({
        "longitude": 0, "declination": 10},
        {"longitude": 0, "declination": -20}
    )

    assert midpoint.declination == -5


def test_create_longitude_velocity_midpoint__none():
    """
    Tests creating a midpoint with average longitude velocity with a missing value.
    """
    midpoint = create_test_midpoint({
        "longitude": 0, "longitude_velocity": 10},
        {"longitude": 0}
    )

    assert midpoint.longitude_velocity is None


def test_create_longitude_velocity_midpoint_valid():
    """
    Tests creating a midpoint with average longitude velocity.
    """
    midpoint = create_test_midpoint({
        "longitude": 0, "longitude_velocity": 10},
        {"longitude": 0, "longitude_velocity": -20}
    )

    assert midpoint.longitude_velocity == -5


def test_create_declination_velocity_midpoint__none():
    """
    Tests creating a midpoint with average declination velocity with a missing value.
    """
    midpoint = create_test_midpoint({
        "longitude": 0},
        {"longitude": 0, "declination_velocity": -20}
    )

    assert midpoint.declination_velocity is None


def test_create_declination_velocity_midpoint__valid():
    """
    Tests creating a midpoint with average declination velocity.
    """
    midpoint = create_test_midpoint({
        "longitude": 0, "declination_velocity": 10},
        {"longitude": 0, "declination_velocity": -20}
    )

    assert midpoint.declination_velocity == -5
