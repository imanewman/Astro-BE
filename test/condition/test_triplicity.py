from astro.chart.condition.triplicity import calculate_triplicity
from astro.schema import PointSchema
from astro.util import Point, ZodiacSign
from test.utils import create_test_points


def create_moon(sign: ZodiacSign, is_day_time: bool = True) -> PointSchema:
    """
    Creates a moon and calculates its triplicity lords.

    :param sign: The sign of the moon.
    :param is_day_time: Whether it is day time.

    :return: The moon.
    """

    moon = create_test_points({"sign": sign})[0]

    calculate_triplicity(moon, is_day_time)

    return moon


def test_calculate_triplicity_day():
    """
    Tests calculating the triplicity rulers during the day of a point.
    """

    moon = create_moon(ZodiacSign.libra)

    assert moon.condition.in_triplicity is False
    assert moon.rulers.triplicity == (Point.saturn, Point.mercury, Point.jupiter)


def test_calculate_triplicity_night():
    """
    Tests calculating the triplicity rulers during the night of a point.
    """

    moon = create_moon(ZodiacSign.libra, False)

    assert moon.condition.in_triplicity is False
    assert moon.rulers.triplicity == (Point.mercury, Point.saturn, Point.jupiter)


def test_calculate_triplicity_ruler():
    """
    Tests calculating whether a point is in the triplicity rulers.
    """

    moon = create_moon(ZodiacSign.taurus, False)

    assert moon.condition.in_triplicity is True
