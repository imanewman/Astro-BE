from datetime import datetime, timedelta

from astro.chart.point.ephemeris import get_julian_day
from astro.schema import EventSchema, EventSettingsSchema
from astro.util import EventType, Point, calculated_points, modern_points, centaur_points, \
    primary_asteroid_points, traditional_points, major_aspects, eighth_harmonic_aspects, declination_aspects, \
    lot_points, lunar_nodes, TransitType, TransitGroupType


def local_event() -> EventSettingsSchema:
    """
    A local location.
    """
    return EventSettingsSchema(
        event=EventSchema(
            name="Transits",
            latitude=47.6769,
            longitude=-122.2060,
            type=EventType.transit,
            utc_date=datetime.utcnow().astimezone(),
            local_date=datetime.now(),
            utc_offset="UTC-8.00",
            # utc_offset="UTC-4.00"
        ),
        enabled=[
            {
                "points": [
                    # Point.moon,
                    Point.mercury,
                    Point.venus,
                    Point.sun,
                    Point.mars,
                    Point.jupiter,
                    Point.saturn,
                    *modern_points,
                    *centaur_points,
                    *primary_asteroid_points,
                ],
                "aspects": [
                    *major_aspects,
                    *eighth_harmonic_aspects,
                    *declination_aspects,
                ]
            },
            {"points": [], "aspects": []}  # Keeps proper aspects in transits
        ]
    )


omega_event = EventSettingsSchema(
    event=EventSchema(
        latitude=47.6769,
        longitude=-122.2060,
        type=EventType.transit,
        local_date="2028-12-12T05:12:00.000Z",
        utc_date="2028-12-12T12:12:00.000Z",
        utc_offset="UTC-7.00"
    ),
    enabled=[
        {
            "points": [
                *traditional_points,
                *lunar_nodes,
                *modern_points,
            ],
            "aspects": [
                *major_aspects,
                *eighth_harmonic_aspects,
                *declination_aspects,
            ]
        }
    ]
)

tim_natal = EventSettingsSchema(
    event=EventSchema(
        name="Tim Newman",
        timezone="America/New_York",
        utc_offset="UTC-4.00",
        local_date="1997-10-11T11:09:00.000Z",
        utc_date="1997-10-11T15:09:00.000Z",
        location="Tisch Hospital, Manhattan, New York, NY, USA",
        latitude=40.7422,
        longitude=-73.9740,
        type=EventType.natal,
        tags=["Me"]
    ),
    enabled=[
        {
            "points": [
                *calculated_points,
                *traditional_points,
                *lunar_nodes,
                *modern_points,
                *centaur_points,
                *primary_asteroid_points,
            ],
            "aspects": [
                *major_aspects,
                *eighth_harmonic_aspects,
                *declination_aspects,
            ]
        },
        {
            "points": lot_points,
            "aspects": major_aspects
        },
    ]
)
"""
The date time of Tim's birth.
"""

tim_natal.event.julian_day = get_julian_day(tim_natal.event.utc_date)


def tim_transits(
        transit_type: TransitType = TransitType.transit_to_chart,
        group_by: TransitGroupType = TransitGroupType.by_day
) -> EventSettingsSchema:
    """
    Settings for Tim Natal X Transits.

    :param transit_type: The type of transits to calculate.
    :param group_by: How to group transits.
    """
    return EventSettingsSchema(**{
        **tim_natal.dict(),
        "transits": {
            "do_calculate_ecliptic": True,
            "do_calculate_precession_corrected": True,
            "do_calculate_declination": True,
            "type": transit_type,
            "group_by": group_by,
            "event": {
                **local_event().event.dict(),
                "utc_end_date": datetime.utcnow().astimezone() + timedelta(days=3),
                "local_end_date": datetime.now() + timedelta(days=3),
            },
            "enabled": local_event().enabled
        }
    })
