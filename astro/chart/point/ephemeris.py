from datetime import datetime
from typing import Tuple

import swisseph as swe


swe.set_ephe_path()


def get_julian_day(timestamp: datetime) -> float:
    """
    Returns the julian day float associated with the given time.

    :param timestamp: The time to use.

    :return: The julian day for that time.
    """

    hours = timestamp.hour + (timestamp.minute / 60)

    return swe.julday(timestamp.year, timestamp.month, timestamp.day, hours)


def get_point_properties(jul_day: float, swe_id: int) -> Tuple[float, float, float]:
    """
    Calculates the degrees from aries, declination, and speed of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :returns:
        [0] The degrees, out of 360, of this point relative to 0 degrees aries.
        [1] The declination of this point above or below the ecliptic.
        [2] The degrees and the minutes of the points speed.
    """

    return get_degrees_from_aries(jul_day, swe_id), \
        get_declination(jul_day, swe_id), \
        get_speed(jul_day, swe_id)


def get_degrees_from_aries(jul_day: float, swe_id: int) -> float:
    """
    Calculates the degrees from aries of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :return: The degrees, out of 360, of this point relative to 0 degrees aries.
    """

    return swe.calc_ut(jul_day, swe_id)[0][0]


def get_declination(jul_day: float, swe_id: int) -> float:
    """
    Calculates the declination of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :return: The degrees, out of 360, of this point relative to 0 degrees aries.
    """

    return swe.calc_ut(
        jul_day, swe_id,
        swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_EQUATORIAL
    )[0][1]


def get_speed(jul_day: float, swe_id: int) -> float:
    """
    Calculates the speed of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :return: The degrees and the minutes of the points speed.
    """

    return swe.calc_ut(jul_day, swe_id,  swe.FLG_SPEED)[0][3]


def get_asc_mc(jul_day: float, lat: float, long: float) -> Tuple[float, float]:
    """
    Calculates the ascendant and midheaven at a given time and location.

    :param jul_day: The time to find the point at.
    :param lat: The degrees of latitude.
    :param long: The degrees of longitude.

    :return:
        [0] The degrees, out of 360, of the ascendant relative to 0 degrees aries.
        [1] The degrees, out of 360, of the midheaven relative to 0 degrees aries.
    """

    houses_and_points = swe.houses(jul_day, lat, long, b'A')
    ascendant = houses_and_points[1][0]
    midheaven = houses_and_points[1][1]

    return ascendant, midheaven
