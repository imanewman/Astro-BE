from typing import Dict, List, Tuple

from astro.schema import PointInTime, HousePlacement
from astro.util import zodiac_sign_order, Point, zodiac_sign_traits, ZodiacSign


def calculate_houses(points: Dict[Point, PointInTime]) -> List[HousePlacement]:
    """
    Calculates the whole sign houses for each point, and calculates
    the traditional rulers for each sign.

    :param points: A collection of points and planets at a certain time.
    """

    houses, house_signs = calculate_whole_sign_houses(points[Point.ascendant])

    for point in points.values():
        calculate_house_of_point(point, houses)

    calculate_traditional_house_rulers(points, house_signs)

    return houses


def calculate_whole_sign_houses(asc: PointInTime) -> Tuple[List[HousePlacement], List[ZodiacSign]]:
    """
    Calculates a 12 item list of the signs in each house, with index 0 being the 1st house.

    :param asc: The current ascendant point.

    :return: The signs in each house
    """

    zodiac_index_of_ascendant = zodiac_sign_order.index(asc.sign)
    houses = []
    house_signs = []

    for house in range(12):
        house_placement = HousePlacement(
            number=house + 1,
            sign=zodiac_sign_order[(zodiac_index_of_ascendant + house) % 12]
        )

        houses.append(house_placement)
        house_signs.append(house_placement.sign)

    return houses, house_signs


def calculate_house_of_point(point: PointInTime, houses: List[HousePlacement]):
    """
    Calculates what house a point falls in.

    :param point: The point to find.
    :param houses: The sign current order of houses.
    :return:
    """

    for house in houses:
        if house.sign == point.sign:
            point.house = house.number

            house.points.append(point.name)

            return


def calculate_traditional_house_rulers(
        points: Dict[Point, PointInTime],
        house_signs: List[ZodiacSign]
):
    """
    Calculates the houses that the traditional planets rule.

    :param points: A collection of points and planets at a certain time.
    :param house_signs: The sign current order of houses.
    """

    for sign, traits in zodiac_sign_traits.signs.items():
        ruler = points[traits.rulership]
        house_ruled = house_signs.index(sign) + 1

        ruler.ruled_houses.append(house_ruled)
