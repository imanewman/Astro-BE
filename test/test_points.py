import pytest

from astro.chart import create_point
from astro.util import tim_natal, Point


def test_create_point():
    """
    Tests that a points location and speed is correctly calculated.
    """

    point_in_time = create_point(tim_natal, Point.saturn)

    assert round(point_in_time.degrees_from_aries, 2) == 16.79
    assert round(point_in_time.declination, 2) == 4.05
    assert round(point_in_time.speed, 3) == -0.079
