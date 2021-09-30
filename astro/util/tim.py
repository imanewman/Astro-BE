from astro.chart.point.ephemeris import get_julian_day
from astro.schema import EventSchema, EventSettingsSchema

local_event = EventSettingsSchema(
    event=EventSchema(
        latitude=47.6769,
        longitude=-122.2060
    )
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
        type="Natal",
        tags=["Me"]
    )
)
"""
The date time of Tim's birth.
"""

tim_natal.event.julian_day = get_julian_day(tim_natal.event.utc_date)
