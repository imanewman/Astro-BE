import pytest

from astro.chart import create_point
from astro.util import tim_natal, Point


def test_create_point():
    """
    Tests that a points location and speed is correctly calculated.
    """

    point_in_time = create_point(tim_natal, Point.saturn)

    assert point_in_time.degrees_from_aries == pytest.approx(16.79)
    assert point_in_time.declination == pytest.approx(4.05)
    assert point_in_time.speed == pytest.approx(-0.079, abs=1e-3)
