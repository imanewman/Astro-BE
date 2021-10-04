from typing import Dict, List

from astro.chart import calculate_point_attributes
from astro.schema import PointSchema
from astro.util import Point


def create_test_points(*point_args: Dict, do_init_point: bool = False) -> List[PointSchema]:
    """
    Creates points with different attributes.
    Point names are iterated in the chaldean order.

    :param point_args: A list of point args to map to created points.
    :param do_init_point: If true, point attributes will be initialized..

    :return: A list of created points in time.
    """

    names = [name.value for name in Point]
    points = []

    for args, point_name in zip(point_args, names):
        if "name" not in args:
            args["name"] = point_name

        if "degrees_from_aries" not in args:
            args["degrees_from_aries"] = 0

        point = PointSchema(**args)

        if do_init_point:
            calculate_point_attributes(point)

        points.append(point)

    return points
