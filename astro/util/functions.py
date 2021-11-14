from astro.util import Point, point_axis_list


def convert_to_degrees(degrees: int, minutes: int, seconds: int) -> float:
    """
    Converts degrees given in whole numbers to the float equivalent.

    :param degrees: The current degrees out of 360.
    :param minutes: The current minutes out of 60.
    :param seconds: The current seconds out of 60.

    :return: The combined degrees as a float.
    """
    return degrees + (minutes / 60) + (seconds / 60 / 60)


def do_points_form_axis(from_point: Point, to_point: Point) -> bool:
    """
    Returns whether the two paints together form an axis.

    :param from_point: The first point.
    :param to_point: The second point.

    :return: Whether the points form an axis.
    """
    return [from_point, to_point] in point_axis_list \
        or [to_point, from_point] in point_axis_list
