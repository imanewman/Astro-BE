from astro import create_summary, calculate_condition, calculate_is_day_time
from astro.chart.point import create_points_with_attributes
from astro.schema import PointSchema
from astro.util import ZodiacSign, Point
from astro.util.test_events import tim_natal


def test_create_summary():
    """
    Tests that the summary planets are properly calculated.
    """

    points = create_points_with_attributes(tim_natal)

    calculate_condition(points, True)

    summary = create_summary(points, True)

    assert summary.sun == ZodiacSign.libra
    assert summary.moon == ZodiacSign.aquarius
    assert summary.asc == ZodiacSign.sagittarius
    assert summary.is_day_time is True


def test_calculate_is_day_time():
    """
    Tests that sect is properly calculated.
    """

    def calculate(sun_longitude: float, asc_longitude: float) -> bool:
        return calculate_is_day_time({
            Point.ascendant: PointSchema(
                name=Point.ascendant,
                points=[Point.ascendant],
                longitude=asc_longitude
            ),
            Point.sun: PointSchema(
                name=Point.sun,
                points=[Point.sun],
                longitude=sun_longitude
            ),
        })

    assert calculate(180, 190) is True
    assert calculate(180, 170) is False
    assert calculate(350, 0) is True
    assert calculate(10, 0) is False


