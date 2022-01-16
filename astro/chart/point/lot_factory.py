from typing import Optional, Dict

from astro.collection.lot_traits import lot_traits
from astro.schema import PointSchema
from astro.util import Point, lot_points


def create_lot(
        points: Dict[Point, PointSchema],
        lot: Point,
        is_day_time: bool
) -> Optional[PointSchema]:
    """
    Creates the given Egyptian/Arabic lot, if all required points exist.

    - Discussion about calculation of declination and velocity:
      https://groups.io/g/swisseph/topic/lots_parts_declinations/76787239

    :param points: The current calculated points.
    :param lot: The lot to create.
    :param is_day_time: Whether it is day time.

    :return: The created lot point.
    """
    if lot not in lot_points or lot not in lot_traits.lots:
        return

    traits = lot_traits.lots[lot]

    if Point.ascendant not in points or \
            traits.add_point not in points or \
            traits.sub_point not in points:
        return

    asc = points[Point.ascendant]
    add_point = points[traits.add_point]
    sub_point = points[traits.sub_point]

    if not is_day_time and traits.reverse_at_night:
        longitude = (asc.longitude + sub_point.longitude - add_point.longitude) % 360
        longitude_velocity = \
            asc.longitude_velocity + sub_point.longitude_velocity - add_point.longitude_velocity
    else:
        longitude = (asc.longitude + add_point.longitude - sub_point.longitude) % 360
        longitude_velocity = \
            asc.longitude_velocity + add_point.longitude_velocity - sub_point.longitude_velocity

    return PointSchema(
        name=lot,
        points=[Point.ascendant, traits.add_point, traits.sub_point],
        longitude=longitude,
        longitude_velocity=longitude_velocity,
    )
