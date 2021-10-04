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


def get_point_properties(jul_day: float, swe_id: int) -> Tuple[float, float, float, float]:
    """
    Calculates the degrees from aries, declination, and speed of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :returns:
        [0] The longitude of this point in degrees.
        [1] The longitude speed per day of this point in degrees.
        [2] The declination of this point in degrees.
        [3] The declination speed per day of this point in degrees.
    """

    longitude, longitude_speed = get_longitude_and_speed(jul_day, swe_id)
    declination, declination_speed = get_declination_and_speed(jul_day, swe_id)

    return longitude, longitude_speed, declination, declination_speed


def get_longitude_and_speed(jul_day: float, swe_id: int) -> Tuple[float, float]:
    """
    Calculates the ecliptic longitude and longitude speed of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :return:
        [0] The ecliptic longitude of this point in degrees.
        [1] The ecliptic longitude speed per day of this point in degrees.
    """

    # [0] ecliptic longitude degrees.
    # [1] ecliptic latitude degrees.
    # [2] ???
    # [3] ecliptic longitude degrees per day.
    # [4] ecliptic latitude degrees per day.
    ecliptic_calculations = swe.calc_ut(jul_day, swe_id,  swe.FLG_SPEED)[0]

    return ecliptic_calculations[0], ecliptic_calculations[3]


def get_declination_and_speed(jul_day: float, swe_id: int) -> Tuple[float, float]:
    """
    Calculates the equatorial declination and declination speed of a point at a given time.

    :param jul_day: The julian day time to find the point at.
    :param swe_id: The swiss ephemeris ID of the point.

    :return:
        [0] The equatorial declination of this point in degrees.
        [1] The equatorial declination speed per day of this point in degrees.
    """

    # [0] equatorial right ascension degrees.
    # [1] equatorial declination degrees.
    # [2] ???
    # [3] equatorial right ascension degrees per day.
    # [4] equatorial declination degrees per day.
    equatorial_calculations = swe.calc_ut(
        jul_day, swe_id,
        swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_EQUATORIAL
    )[0]

    return equatorial_calculations[1], equatorial_calculations[4]


def get_angles(
        jul_day: float,
        lat: float,
        long: float
) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """
    Calculates the longitude and declination of the Ascendant, MC, Descendant, IC, and Vertex.

    - Notes how to calculate declination: `

    :param jul_day: The time to find the point at.
    :param lat: The degrees of latitude of the event.
    :param long: The degrees of longitude of the event.

    :return:
        [0] The ecliptic longitude and equatorial declination of the Ascendant.
        [1] The ecliptic longitude and equatorial declination of the Midheaven.
        [2] The ecliptic longitude and equatorial declination of the Descendant.
        [3] The ecliptic longitude and equatorial declination of the IC.
        [4] The ecliptic longitude and equatorial declination of the Vertex.
    """

    houses_and_points = swe.houses(jul_day, lat, long, b'A')
    asc = houses_and_points[1][0]
    mc = houses_and_points[1][1]
    desc = (asc + 180) % 360
    ic = (mc + 180) % 360
    vertex = houses_and_points[1][3]

    # [0] True obliquity of the ecliptic.
    # [1] Mean obliquity of the ecliptic.
    # [2] Nutation in longitude.
    # [2] Nutation in obliquity.
    obliquity_and_nutation = swe.calc_ut(jul_day, swe.ECL_NUT)[0]
    obliquity = obliquity_and_nutation[0]

    asc_declination = swe.cotrans(asc, 0, 1, -obliquity)[1]
    mc_declination = swe.cotrans(mc, 0, 1, -obliquity)[1]
    desc_declination = swe.cotrans(desc, 0, 1, -obliquity)[1]
    ic_declination = swe.cotrans(ic, 0, 1, -obliquity)[1]
    vertex_declination = swe.cotrans(vertex, 0, 1, -obliquity)[1]

    return (
        (asc, asc_declination),
        (mc, mc_declination),
        (desc, desc_declination),
        (ic, ic_declination),
        (vertex, vertex_declination),
    )
