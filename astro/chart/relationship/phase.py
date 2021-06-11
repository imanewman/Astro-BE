from typing import Optional, Tuple

from astro.schema import RelationshipSchema, PointSchema
from astro.util import point_traits, Point, PhaseType


def calculate_aspect_phase(
        relationship: RelationshipSchema,
        from_point: PointSchema,
        to_point: PointSchema,
):
    """
    Calculates the phase between two planets zodiacal positions.

    - If one of the given planets doesn't have traits or a speed:
        - Sets the relationship's `degrees_between` from the first to the second point.
    - If both planets have a speed:
        - Sets the relationship's `degrees_between` from the slower to the faster point.
        - Sets the relationship's `phase_base_point` and `phase` attributes.
        - For inferior planets cycles to the sun, separate calculations are done to determine the `phase`.

    :param relationship: The relationship between points to store calculations in.
    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.
    """

    # Set a placeholder degrees between in case one of the points doesn't have a speed
    relationship.degrees_between = calculate_degrees_between(from_point, to_point)

    # Find which body has the slower speed, which is used as the fulcrum
    slower, faster = calculate_faster_point(from_point, to_point)

    # Avoid calculations for planets without speeds
    if not slower or not faster:
        return

    # Set the slower point as the base for calculations of phase
    relationship.phase_base_point = slower.name
    relationship.degrees_between = calculate_degrees_between(slower, faster)

    point_names = [from_point.name, to_point.name]

    # Avoid calculations for inferior planets to the sun, which cannot make a complete cycle
    if Point.sun in point_names and (Point.venus in point_names or Point.mercury in point_names):
        calculate_inferior_aspect_phase(relationship, faster)
    else:
        calculate_superior_aspect_phase(relationship)


def calculate_degrees_between(slower: PointSchema, faster: PointSchema) -> float:
    """
    calculate the degrees of phase from the slower to the faster planet.

    :param slower: The point to calculate degrees from.
    :param faster: The point to calculate degrees to.

    :return: The degrees out of 360 from the slower to the faster planet.
    """

    return round(faster.degrees_from_aries - slower.degrees_from_aries, 2) % 360


def calculate_faster_point(
        from_point: PointSchema,
        to_point: PointSchema
) -> Tuple[Optional[PointSchema], Optional[PointSchema]]:
    """
    Calculates which point is faster.

    - If one of the given planets doesn't have traits or a speed, no points are returned.

    :param from_point: The starting point in the relationship.
    :param to_point: The ending point in the relationship.

    :return:
        [0] The faster point, if one exists.
        [1] The slower point, if one exists.
    """

    # Avoid calculations for planets without traits
    if from_point.name not in point_traits.points or to_point.name not in point_traits.points:
        return None, None

    from_speed = point_traits.points[from_point.name].speed_avg
    to_speed = point_traits.points[to_point.name].speed_avg

    # Avoid calculations for planets without speeds
    if not from_speed or not to_speed:
        return None, None

    # find which body has the slower speed
    return (from_point, to_point) if from_speed < to_speed else (to_point, from_point)


def calculate_superior_aspect_phase(relationship: RelationshipSchema):
    """
    Calculates the aspect phase between any points that make a complete zodiacal cycle.

    - Sets the relationship's `phase` attribute.

    :param relationship: The relationship between points to store calculations in.
    """

    if relationship.degrees_between < 45:
        relationship.phase = PhaseType.new
    elif 45 <= relationship.degrees_between < 90:
        relationship.phase = PhaseType.crescent
    elif 90 <= relationship.degrees_between < 135:
        relationship.phase = PhaseType.first_quarter
    elif 135 <= relationship.degrees_between < 180:
        relationship.phase = PhaseType.gibbous
    elif 180 <= relationship.degrees_between < 225:
        relationship.phase = PhaseType.full
    elif 225 <= relationship.degrees_between < 270:
        relationship.phase = PhaseType.disseminating
    elif 270 <= relationship.degrees_between < 315:
        relationship.phase = PhaseType.last_quarter
    elif 315 <= relationship.degrees_between:
        relationship.phase = PhaseType.balsamic


def calculate_inferior_aspect_phase(relationship: RelationshipSchema, faster: PointSchema):
    """
    Calculates the aspect phase between the Sun and Mercury or Venus.

    - Neither make a complete zodiacal cycle relative to the Sun, changing phase calculations.
    - Each cycle begins and ends with the retrograde conjunction of the planet with the Sun.
    - Sets the relationship's `phase` attribute.

    :param relationship: The relationship between points to store calculations in.
    :param faster: The faster point in the relationship, either Mercury or Venus.
    """

    if relationship.degrees_between > 180:
        if faster.speed < 0:
            # The cycle begins with the retrograde conjunction with the Sun
            relationship.phase = PhaseType.new
        else:
            relationship.phase = PhaseType.first_quarter
    else:
        if faster.speed < 0:
            # The cycle ends with the retrograde conjunction with the Sun
            relationship.phase = PhaseType.last_quarter
        else:
            relationship.phase = PhaseType.full
