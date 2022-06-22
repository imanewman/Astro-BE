from datetime import timedelta
from typing import List, Optional, Dict

from astro.chart.point.point_attributes import calculate_sign
from astro.schema import EventSettingsSchema, TransitSchema, PointSchema
from astro.util import AspectMovementType, EventType, TransitType


def calculate_all_points_timing(
        base_event_settings: EventSettingsSchema,
        current_event_settings: EventSettingsSchema,
        current_points: Dict[str, PointSchema],
        last_points: Dict[str, PointSchema],
        is_one_chart: bool
) -> List[TransitSchema]:
    """
    Calculates the timing of all points making ingresses and stationing.

    :param base_event_settings: The base time, location, enabled points, and transit settings.
    :param current_event_settings: The event for the current moment.
    :param current_points: The points at the current time.
    :param last_points: The points at the last time.
    :param is_one_chart: If false, no ingresses or stations will be calculated.

    :return: All calculated transits.
    """
    transits = []

    if not is_one_chart or not base_event_settings.transits.do_calculate_points():
        return transits

    for last_point in last_points.values():
        current_point = current_points[last_point.name]

        if not current_point:
            continue

        for transit in calculate_point_timing(
                base_event_settings, current_event_settings,
                current_point, last_point
        ):
            transits.append(transit)

    return transits


def calculate_point_timing(
        base_event_settings: EventSettingsSchema,
        current_event_settings: EventSettingsSchema,
        current_point: PointSchema,
        last_point: PointSchema,
) -> List[TransitSchema]:
    """
    Calculates the timing of points making ingresses and stationing.

    :param base_event_settings: The base time, location, enabled points, and transit settings.
    :param current_event_settings: The event for the current moment.
    :param current_point: The point at the current time.
    :param last_point: The point at the last time.

    :return: All calculated transits.
    """
    transit_settings = base_event_settings.transits
    transits = []

    if transit_settings.do_calculate_ingress:
        ingress = calculate_ingress_timing(current_event_settings, current_point, last_point)

        if ingress:
            transits.append(ingress)

    if transit_settings.do_calculate_station:
        station = calculate_station_timing(current_event_settings, current_point, last_point)

        if station:
            transits.append(station)

    return transits


def calculate_ingress_timing(
        current_event_settings: EventSettingsSchema,
        current_point: PointSchema,
        last_point: PointSchema,
) -> Optional[TransitSchema]:
    """
    Calculates the timing of points making ingresses.

    :param current_event_settings: The event for the current moment.
    :param current_point: The point at the current time.
    :param last_point: The point at the last time.

    :return: The calculated ingress, if there is one.
    """
    last_sign = calculate_sign(last_point.longitude)
    current_sign = calculate_sign(current_point.longitude)

    if last_sign is current_sign:
        return

    if current_point.longitude_velocity > 0:
        orb = -(current_point.longitude % 30)
        transit_type = TransitType.ingress_direct
    else:
        orb = (30 - current_point.longitude % 30)
        transit_type = TransitType.ingress_retrograde

    approximate_days_until_exact = orb / current_point.longitude_velocity
    time_delta = timedelta(days=approximate_days_until_exact)
    local_exact_date = current_event_settings.event.local_date + time_delta
    utc_exact_date = current_event_settings.event.utc_date + time_delta
    name = f"{current_point.name} {transit_type} Into {current_sign}"

    return TransitSchema(**{
        "from_point": current_point.name,
        "to_point": current_point.name,
        "from_type": EventType.transit,
        "to_type": EventType.transit,
        "name": name,
        "transit_type": transit_type,
        "sign": current_sign,
        "local_exact_date": local_exact_date,
        "utc_exact_date": utc_exact_date,
        "movement": AspectMovementType.exact
    })


def calculate_station_timing(
        current_event_settings: EventSettingsSchema,
        current_point: PointSchema,
        last_point: PointSchema,
) -> Optional[TransitSchema]:
    """
    Calculates the timing of points stationing.

    :param current_event_settings: The event for the current moment.
    :param current_point: The point at the current time.
    :param last_point: The point at the last time.

    :return: The calculated station, if there is one.
    """
    last_is_positive = last_point.longitude_velocity > 0
    current_is_positive = current_point.longitude_velocity > 0

    if last_is_positive is current_is_positive:
        return

    current_sign = calculate_sign(current_point.longitude)
    local_exact_date = current_event_settings.event.local_date
    utc_exact_date = current_event_settings.event.utc_date
    transit_type = TransitType.station_direct if current_is_positive else TransitType.station_retrograde
    name = f"{current_point.name} {transit_type} In {current_sign}"

    return TransitSchema(**{
        "from_point": current_point.name,
        "to_point": current_point.name,
        "from_type": EventType.transit,
        "to_type": EventType.transit,
        "name": name,
        "transit_type": transit_type,
        "sign": current_sign,
        "local_exact_date": local_exact_date,
        "utc_exact_date": utc_exact_date,
        "movement": AspectMovementType.exact,
    })
