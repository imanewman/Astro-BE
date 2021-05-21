from astro import create_all_points, create_summary
from astro.chart import calculate_is_day_time
from astro.util import tim_natal, ZodiacSign, Point


def test_create_summary():
    """
    Tests that the summary planets are properly calculated.
    """

    points = create_all_points(tim_natal)
    summary = create_summary(points)

    assert summary.sun == ZodiacSign.libra
    assert summary.moon == ZodiacSign.aquarius
    assert summary.asc == ZodiacSign.sagittarius
    assert summary.asc_ruler == Point.jupiter
    assert summary.is_day_time is True


def test_calculate_is_day_time():
    """
    Tests that sect is properly calculated.
    """

    assert calculate_is_day_time(180, 190) is True
    assert calculate_is_day_time(180, 170) is False
    assert calculate_is_day_time(350, 0) is True
    assert calculate_is_day_time(10, 0) is False


