from typing import Dict, List

from astro.schema import PointInTime
from astro.util import zodiacSignOrder, Point, zodiacSignTraits, ZodiacSign


def calculate_houses(points: Dict[Point, PointInTime]) -> List[ZodiacSign]:
    """
    Calculates the whole sign houses for each point, and calculates
    the traditional rulers for each sign.

    :param points: A collection of points and planets at a certain time.
    """

    houses = calculate_whole_sign_houses(points[Point.ascendant])

    for point in points.values():
        point.house = calculate_house_of_sign(point.sign, houses)

    calculate_traditional_house_rulers(points, houses)

    return houses


def calculate_house_of_sign(sign: ZodiacSign, houses: List[ZodiacSign]):
    """
    Calculates what house a sign falls in.

    :param sign: The zodiac sign to look for.
    :param houses: The sign current order of houses.
    :return:
    """

    return houses.index(sign) + 1


def calculate_whole_sign_houses(asc: PointInTime) -> List[ZodiacSign]:
    """
    Calculates a 12 item list of the signs in each house, with index 0 being the 1st house.

    :param asc: The current ascendant point.

    :return: The signs in each house
    """

    zodiac_index_of_ascendant = zodiacSignOrder.index(asc.sign)
    houses = []

    for house in range(12):
        current_sign = zodiacSignOrder[(zodiac_index_of_ascendant + house) % 12]

        houses.append(current_sign)

    return houses


def calculate_traditional_house_rulers(points: Dict[Point, PointInTime], houses: List[ZodiacSign]):
    """
    Calculates the houses that the traditional planets rule.

    :param points: A collection of points and planets at a certain time.
    :param houses: The sign current order of houses.
    """

    for sign, traits in zodiacSignTraits.signs.items():
        ruler = points[traits.rulership]
        house_ruled = calculate_house_of_sign(sign, houses)

        ruler.ruled_houses.append(house_ruled)

