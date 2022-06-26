from datetime import timedelta
from typing import List, Optional

from astro.schema import EventSettingsSchema, TransitSchema, PointSchema, TransitIncrement
from astro.util import AspectMovementType, EventType, TransitType


def calculate_all_points_timing(
        base_event_settings: EventSettingsSchema,
        current_increment: TransitIncrement,
        last_increment: TransitIncrement,
) -> List[TransitSchema]:
    """
    Calculates the timing of all points making ingresses and stationing.

    :param base_event_settings: The base time, location, enabled points, and transit settings.
    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param last_increment: The last [0] event, [1] points, and [2] relationships.

    :return: All calculated transits.
    """
    last_points, current_points = last_increment[1], current_increment[1]
    settings = base_event_settings.transits
    transits = []

    if not settings.is_one_chart() or not settings.do_calculate_points():
        return transits

    for last_point in last_points.values():
        current_point = current_points[last_point.name]

        if not current_point:
            continue

        for transit in calculate_point_timing(
                base_event_settings, current_increment,
                current_point, last_point
        ):
            transits.append(transit)

    return transits


def calculate_point_timing(
        base_event_settings: EventSettingsSchema,
        current_increment: TransitIncrement,
        current_point: PointSchema,
        last_point: PointSchema,
) -> List[TransitSchema]:
    """
    Calculates the timing of points making ingresses and stationing.

    :param base_event_settings: The base time, location, enabled points, and transit settings.
    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_point: The point at the current time.
    :param last_point: The point at the last time.

    :return: All calculated transits.
    """
    transit_settings = base_event_settings.transits
    transits = []

    if transit_settings.do_calculate_ingress:
        ingress = calculate_ingress_timing(current_increment, current_point, last_point)

        if ingress:
            transits.append(ingress)

    if transit_settings.do_calculate_station:
        station = calculate_station_timing(current_increment, current_point, last_point)

        if station:
            transits.append(station)

    return transits


def calculate_ingress_timing(
        current_increment: TransitIncrement,
        current_point: PointSchema,
        last_point: PointSchema,
) -> Optional[TransitSchema]:
    """
    Calculates the timing of points making ingresses.

    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_point: The point at the current time.
    :param last_point: The point at the last time.

    :return: The calculated ingress, if there is one.
    """
    current_event_settings = current_increment[0]

    if last_point.sign is current_point.sign:
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
    name = f"{current_point.name} {transit_type} Into {current_point.sign}"

    return TransitSchema(
        from_point=current_point.name,
        from_sign=current_point.sign,
        from_type=EventType.transit,
        name=name,
        transit_type=transit_type,
        movement=AspectMovementType.exact,
        local_exact_date=local_exact_date,
        utc_exact_date=utc_exact_date,
    )


def calculate_station_timing(
        current_increment: TransitIncrement,
        current_point: PointSchema,
        last_point: PointSchema,
) -> Optional[TransitSchema]:
    """
    Calculates the timing of points stationing.

    :param current_increment: The current [0] event, [1] points, and [2] relationships.
    :param current_point: The point at the current time.
    :param last_point: The point at the last time.

    :return: The calculated station, if there is one.
    """
    current_event_settings = current_increment[0]
    last_is_positive = last_point.longitude_velocity > 0
    current_is_positive = current_point.longitude_velocity > 0

    if last_is_positive is current_is_positive:
        return

    local_exact_date = current_event_settings.event.local_date
    utc_exact_date = current_event_settings.event.utc_date
    transit_type = TransitType.station_direct if current_is_positive else TransitType.station_retrograde
    name = f"{current_point.name} {transit_type} In {current_point.sign}"

    return TransitSchema(
        from_point=current_point.name,
        from_sign=current_point.sign,
        from_type=EventType.transit,
        name=name,
        transit_type=transit_type,
        local_exact_date=local_exact_date,
        utc_exact_date=utc_exact_date,
        movement=AspectMovementType.exact,
    )
