from typing import Dict, List, Tuple, Optional

from astro.chart.point.ephemeris import get_house_cusps
from astro.schema import PointSchema, HouseSchema, EventSchema
from astro.util import zodiac_sign_order, Point, ZodiacSign, HouseSystem
from astro.collection.zodiac_sign_traits import zodiac_sign_traits

degrees_per_sign = 30
number_of_signs = 12


def calculate_houses(
        points: Dict[Point, PointSchema],
        event: Optional[EventSchema] = None,
        secondary_house_system: HouseSystem = HouseSystem.whole_sign
) -> Tuple[List[HouseSchema], List[HouseSchema]]:
    """
    Calculates the whole sign and secondary houses and related attributes for each point.

    - Sets the `houses_whole_sign` and `houses_secondary` attributes within `points` items.

    :param points: A collection of points at a certain time and location.
    :param event: The event time and location.
    :param secondary_house_system: The secondary house system to use.

    :return:
        [0] A 12 item a list of house objects for each whole sign house.
        [1] A 12 item a list of house objects for each secondary house.
    """
    houses_whole_sign = calculate_whole_sign_houses(points)

    if event is None or secondary_house_system is HouseSystem.whole_sign:
        # Return just whole signs if a secondary house system cannot be calculated.

        return houses_whole_sign, houses_whole_sign
    else:
        # Calculate secondary houses.
        houses_secondary = calculate_secondary_houses(points, event, secondary_house_system)

        return houses_whole_sign, houses_secondary


def calculate_whole_sign_houses(points: Dict[Point, PointSchema]) -> List[HouseSchema]:
    """
    Calculates the whole sign houses and related attributes for each point.

    - Sets the `houses_whole_sign` attributes within `points` items.

    :param points: A collection of points at a certain time and location.

    :return: A 12 item a list of house objects for each whole sign house.
    """
    if Point.ascendant not in points:
        # Skip house calculations if the ascendant point hasn't been calculated.
        return []

    houses_whole_sign, house_signs = calculate_whole_sign_house_cusps(points[Point.ascendant])

    for point in points.values():
        calculate_whole_sign_house_of_point(point, houses_whole_sign)

    calculate_house_rulers(points, houses_whole_sign, True)

    return houses_whole_sign


def calculate_whole_sign_house_cusps(asc: PointSchema) -> Tuple[List[HouseSchema], List[ZodiacSign]]:
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

    for house_number in range(number_of_signs):
        zodiac_sign_number = (zodiac_index_of_ascendant + house_number) % number_of_signs
        house = HouseSchema(
            number=house_number + 1,
            sign=zodiac_sign_order[zodiac_sign_number],
            from_longitude=zodiac_sign_number * degrees_per_sign,
            to_longitude=(zodiac_sign_number + 1) * degrees_per_sign,
        )

        houses.append(house)
        house_signs.append(house.sign)

    return houses, house_signs


def calculate_whole_sign_house_of_point(
        point: PointSchema,
        houses: List[HouseSchema]
):
    """
    Calculates what whole sign house a point falls in.

    - Sets the `houses_whole_sign.house` attribute within the `point`.
    - Defaults the `houses_secondary.house` attribute within the `point` to whole sign.
    - Sets the `points` attribute within `houses` items.

    :param point: The point to find the house of.
    :param houses: The order of houses.
    """
    for house in houses:
        if house.sign == point.sign:
            point.houses_whole_sign.house = house.number
            point.houses_secondary.house = house.number

            house.points.append(point.name)

            return


def calculate_house_rulers(
        points: Dict[Point, PointSchema],
        houses: List[HouseSchema],
        set_primary_houses: bool
):
    """
    Calculates the houses that the traditional planets rule.

    - Sets the `houses_whole_sign.ruled_houses` attribute within `points` items.

    :param points: A collection of points at a certain time and location.
    :param houses: The calculated house cusps.
    :param set_primary_houses: Whether to set primary or secondary house rulers.
    """
    house_number = 0

    for house in houses:
        house_number += 1
        sign_rulers = [
            zodiac_sign_traits.signs[house.sign].domicile_traditional,
            zodiac_sign_traits.signs[house.sign].domicile_modern,
            *zodiac_sign_traits.signs[house.sign].domicile_asteroid,
        ]

        for sign_ruler in sign_rulers:
            if sign_ruler in points:
                ruler = points[sign_ruler]
                whole_sign_houses = ruler.houses_whole_sign.ruled_houses
                secondary_houses = ruler.houses_secondary.ruled_houses

                if set_primary_houses and house_number not in whole_sign_houses:
                    whole_sign_houses.append(house_number)
                elif house_number not in secondary_houses:
                    secondary_houses.append(house_number)


def calculate_secondary_houses(
        points: Dict[Point, PointSchema],
        event: Optional[EventSchema] = None,
        secondary_house_system: HouseSystem = HouseSystem.whole_sign
) -> List[HouseSchema]:
    """
    Calculates the secondary houses and related attributes for each point.

    - Sets the `houses_secondary` attributes within `points` items.

    :param points: A collection of points at a certain time and location.
    :param event: The event time and location.
    :param secondary_house_system: The secondary house system to use.

    :return: A 12 item a list of house objects for each secondary house.
    """
    houses_secondary = calculate_secondary_house_cusps(event, secondary_house_system)

    for point in points.values():
        point.houses_secondary.house_system = secondary_house_system

        calculate_secondary_house_of_point(point, houses_secondary)

    calculate_house_rulers(points, houses_secondary, False)

    return houses_secondary


def calculate_secondary_house_cusps(
        event: EventSchema,
        secondary_house_system: HouseSystem
) -> List[HouseSchema]:
    """
    Calculates 12 items list of house objects for each house.

    :param event: The event time and location.
    :param secondary_house_system: The secondary house system to use.

    :return: A 12 item a list of house objects for each secondary house.
    """
    cusps = get_house_cusps(event.julian_day, event.latitude, event.longitude, secondary_house_system)
    houses = []

    for house_number in range(number_of_signs):
        houses.append(HouseSchema(
            number=house_number + 1,
            sign=zodiac_sign_order[int(cusps[house_number] / degrees_per_sign)],
            from_longitude=cusps[house_number],
            to_longitude=cusps[(house_number + 1) % number_of_signs],
        ))

    return houses


def calculate_secondary_house_of_point(
        point: PointSchema,
        houses: List[HouseSchema]
):
    """
    Calculates what secondary house a point falls in.

    - Sets the `houses_secondary.house` attribute within the `point`.
    - Sets the `points` attribute within `houses` items.

    :param point: The point to find the house of.
    :param houses: The order of houses.
    """
    for house in houses:
        normalized_point_longitude = (point.longitude - house.from_longitude) % 360
        normalized_max_longitude = (house.to_longitude - house.from_longitude) % 360

        if normalized_point_longitude < normalized_max_longitude:
            # If this point is within the arc of this house, track this house for the point.
            point.houses_secondary.house = house.number

            house.points.append(point.name)

            return
