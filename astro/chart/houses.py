from typing import Dict, List, Tuple

from astro.schema import PointSchema, HouseSchema
from astro.util import zodiac_sign_order, Point, zodiac_sign_traits, ZodiacSign


def calculate_houses(points: Dict[Point, PointSchema]) -> List[HouseSchema]:
    """
    Calculates the whole sign houses nad related attributes for each point.

    - Sets the `ruled_houses` and `house` attributes within points items.

    :param points: A collection of points at a certain time and location.
    :return: A 12 item a list of house objects for each whole sign house.
    """

    # Skip house calculations if the ascendant point hasn't been calculated.
    if Point.ascendant not in points:
        return []

    houses, house_signs = calculate_whole_sign_houses(points[Point.ascendant])

    for point in points.values():
        calculate_house_of_point(point, houses)

    calculate_traditional_house_rulers(points, house_signs)

    return houses


def calculate_whole_sign_houses(asc: PointSchema) -> Tuple[List[HouseSchema], List[ZodiacSign]]:
    """
    Calculates 12 items lists of the zodiac signs for each each house, with index 0 being the 1st house.

    :param asc: The current ascendant point.

    :return: The signs in each house.
        [0] A 12 item a list of house objects for each whole sign house.
        [1] A 12 item a list of the zodiac signs for each whole sign house.
    """

    zodiac_index_of_ascendant = zodiac_sign_order.index(asc.sign)
    houses = []
    house_signs = []

    for house_number in range(12):
        house = HouseSchema(
            number=house_number + 1,
            sign=zodiac_sign_order[(zodiac_index_of_ascendant + house_number) % 12]
        )

        houses.append(house)
        house_signs.append(house.sign)

    return houses, house_signs


def calculate_house_of_point(point: PointSchema, houses: List[HouseSchema]):
    """
    Calculates what whole sign house a point falls in.

    - Sets the `house` attribute within the point.
    - Sets the `points` attribute within houses items.

    :param point: The point to find the house of.
    :param houses: The order of houses.
    """

    for house in houses:
        if house.sign == point.sign:
            point.house = house.number

            house.points.append(point.name)

            return


def calculate_traditional_house_rulers(
        points: Dict[Point, PointSchema],
        house_signs: List[ZodiacSign]
):
    """
    Calculates the houses that the traditional planets rule.

    - Sets the `ruled_houses` attribute within points items.

    :param points: A collection of points at a certain time and location.
    :param house_signs: The zodiac sign order of houses.
    """

    for sign, traits in zodiac_sign_traits.signs.items():
        house_ruled = house_signs.index(sign) + 1

        if traits.rulership in points:
            ruler = points[traits.rulership]

            ruler.ruled_houses.append(house_ruled)
