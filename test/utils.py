from typing import Dict, List

from astro.chart import calculate_point_attributes
from astro.schema import PointInTime
from astro.util import Point


def create_test_points(*point_args: Dict, do_init_point: bool = False) -> List[PointInTime]:
    """
    Creates points with different attributes.
    Point names are iterated in the chaldean order.

    :param point_args: A list of point args to map to created points.
    :param do_init_point: If true, point attributes will be initialized..

    :return: A list of created points in time.
    """

    names = [name.value for name in Point][2:]
    points = []

    for args, point_name in zip(point_args, names):
        if "name" not in args:
            args["name"] = point_name

        if "degrees_from_aries" not in args:
            args["degrees_from_aries"] = 0

        point = PointInTime(**args)

        if do_init_point:
            calculate_point_attributes(point)

        points.append(point)

    return points
