import datetime

from astro.chart.point.ephemeris import get_julian_day
from astro.schema import EventSchema, EventSettingsSchema
from astro.util import EventType, Point

local_event = EventSettingsSchema(
    event=EventSchema(
        latitude=47.6769,
        longitude=-122.2060,
        type=EventType.transit,
        utc_date=datetime.datetime.utcnow().astimezone(),
        local_date=datetime.datetime.now(),
        utc_offset="UTC-7.00"
    ),
    enabled_points=[
        Point.moon,
        Point.mercury,
        Point.venus,
        Point.sun,
        Point.mars,
        Point.jupiter,
        Point.saturn,
        Point.uranus,
        Point.neptune,
        Point.pluto,
        Point.north_mode,
        Point.chiron,
        Point.pholus,
        Point.ceres,
        Point.pallas,
        Point.juno,
        Point.vesta,
    ]
)
"""
A local location.
"""

tim_natal = EventSettingsSchema(
    event=EventSchema(
        name="Tim Newman",
        timezone="America/New_York",
        utc_offset="UTC-4.00",
        local_date="1997-10-11T11:09:00.000Z",
        utc_date="1997-10-11T15:09:00.000Z",
        location="Manhattan, New York, NY, USA",
        latitude=40.78343,
        longitude=-73.96625,
        type=EventType.natal,
        tags=["Me"]
    )
)
"""
The date time of Tim's birth.
"""

tim_natal.event.julian_day = get_julian_day(tim_natal.event.utc_date)
