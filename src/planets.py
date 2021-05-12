from typing import List, Tuple

from src.enums import ZodiacSign, Point
from src.globals import pointTraits, zodiacSignOrder, zodiacSignTraits
from src.models import PointInTime, CalculationSettings, CalculationResults
from src.ephemeris import get_julian_day, get_degrees_from_aries, get_declination, get_asc_mc


def create_results(settings: CalculationSettings) -> CalculationResults:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    results = CalculationResults(
        **settings.dict(),
        startPoints=create_all_points(settings)
    )

    create_results_summary(results)

    return results


def create_results_summary(results: CalculationResults):
    """
    Creates a summary of the big 3 signs in a given chart,
    as well as whether the chart is during the day.

    :param results: The current calculation results.
    """

    asc_degrees_from_aries = 0
    sun_degrees_from_aries = 0

    for point in results.startPoints:
        if point.name == Point.ascendant:
            results.asc = point.sign
            results.ascRuler = zodiacSignTraits.signs[point.sign].rulership
            asc_degrees_from_aries = point.degrees_from_aries

        elif point.name == Point.sun:
            results.sun = point.sign
            sun_degrees_from_aries = point.degrees_from_aries

        elif point.name == Point.moon:
            results.moon = point.sign

    positive_difference_in_degrees = (sun_degrees_from_aries - asc_degrees_from_aries) % 360

    results.is_day_time = positive_difference_in_degrees > 180


def create_all_points(settings: CalculationSettings) -> List[PointInTime]:
    """
    Creates a list of all calculated points.

    :param settings: The current calculation settings, including the time and location.

    :return: The calculated points.
    """

    points = []

    # Add the ascendant and midheaven
    asc, mc = create_as_mc(settings)

    points.append(asc)
    points.append(mc)

    # add each of the points with traits
    for point in pointTraits.points:
        points.append(create_point(settings, point))

    # calculate the derived point attributes for each point
    for point in points:
        calculate_point_attributes(point, asc)

    return points


def create_as_mc(settings: CalculationSettings) -> Tuple[PointInTime, PointInTime]:
    """
    Creates the points for the Ascendant and Midheaven

    :param settings: The current calculation settings, including the time and location.

    :return: The ascendant and midheaven points.
    """

    day = get_julian_day(settings.startDate)
    ascendant, midheaven = get_asc_mc(day, settings.latitude, settings.longitude)

    return (
        PointInTime(
            name=Point.ascendant,
            degrees_from_aries=round(ascendant, 2),
        ),
        PointInTime(
            name=Point.midheaven,
            degrees_from_aries=round(midheaven, 2),
        )
    )


def create_point(settings: CalculationSettings, point: Point) -> PointInTime:
    """
    Creates a point object for he given planet on the given day.

    :param settings: The current calculation settings, including the time and location.
    :param point: The point to find.

    :return: The calculated point.
    """

    traits = pointTraits.points[point]
    day = get_julian_day(settings.startDate)
    degrees_from_aries = get_degrees_from_aries(day, traits.swe_id)
    declination = get_declination(day, traits.swe_id)

    point_in_time = PointInTime(
        name=traits.name,
        degrees_from_aries=round(degrees_from_aries, 2),
        declination=round(declination, 2)
    )

    return point_in_time


def calculate_point_attributes(point: PointInTime, asc: PointInTime):
    """
    Calculates all derived attributes for a point.

    :param point: The point to calculate attributes for.
    :param asc: The ascendant point, for calculating house.
    """

    point.sign = calculate_sign(point.degrees_from_aries)
    point.degrees_in_sign = calculate_degrees_in_sign(point.degrees_from_aries)
    point.minutes_in_degree = calculate_minutes_in_degree(point.degrees_from_aries)
    point.house = calculate_whole_sign_house(point, asc)


def calculate_sign(degrees_from_aries: float) -> ZodiacSign:
    twelfth_of_circle = int(degrees_from_aries / 30)

    return zodiacSignOrder[twelfth_of_circle]


def calculate_degrees_in_sign(degrees_from_aries: float) -> int:
    return int(degrees_from_aries % 30)


def calculate_minutes_in_degree(degrees_from_aries: float) -> int:
    fraction_of_degree = degrees_from_aries % 1
    degrees_per_minute = 60

    return int(fraction_of_degree * degrees_per_minute)


def calculate_whole_sign_house(point: PointInTime, asc: PointInTime) -> int:
    index_of_ascendant = zodiacSignOrder.index(asc.sign)
    index_of_point = zodiacSignOrder.index(point.sign)
    difference_in_index = index_of_point - index_of_ascendant

    return difference_in_index % 12 + 1
