from typing import Any

import swisseph as swe

from src.enums import ZodiacSign, Point
from src.globals import pointTraits
from src.models import PointInTime


def create_point(day: Any, point: Point) -> PointInTime:
    """
    Creates a point object for he given planet on the given day.

    :param day: The day to find the location of the point for
    :param point: The point to find.

    :return point_in_time: The calculated point.
    """

    traits = pointTraits.points[point]

    # Calculate the current degrees from aries of the point
    degrees_from_aries = swe.calc_ut(day, traits.swe_id)[0][0]

    # Calculate the declination of the point
    declination = swe.calc_ut(
        day, traits.swe_id,
        swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_EQUATORIAL
    )[0][1]

    point_in_time = PointInTime(
        name=traits.name,
        degrees_from_aries=round(degrees_from_aries, 2),
        declination=round(declination, 2)
    )

    calculate_point_attributes(point_in_time)

    return point_in_time


def calculate_point_attributes(point: PointInTime):
    """
    Calculates all derived attributes for a point.

    :param point: The point to calculate attributes for.
    """

    point.sign = calculate_sign(point.degrees_from_aries)
    point.degrees_in_sign = calculate_degrees_in_sign(point.degrees_from_aries)
    point.minutes_in_degree = calculate_minutes_in_degree(point.degrees_from_aries)


def calculate_sign(degrees_from_aries: float) -> ZodiacSign:
    return [
        ZodiacSign.aries,
        ZodiacSign.taurus,
        ZodiacSign.gemini,
        ZodiacSign.cancer,
        ZodiacSign.leo,
        ZodiacSign.virgo,
        ZodiacSign.libra,
        ZodiacSign.scorpio,
        ZodiacSign.sagittarius,
        ZodiacSign.capricorn,
        ZodiacSign.aquarius,
        ZodiacSign.pisces
    ][int(degrees_from_aries / 30)]


def calculate_degrees_in_sign(degrees_from_aries: float) -> int:
    return int(degrees_from_aries % 30)


def calculate_minutes_in_degree(degrees_from_aries: float) -> int:
    return int(degrees_from_aries % 1 * 60)
