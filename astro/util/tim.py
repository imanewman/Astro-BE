from astro.chart.point.ephemeris import get_julian_day
from astro.schema import EventSchema

"""
The date time of Tim's birth.
"""
tim_natal = EventSchema(
    utc_date="1997-10-11T15:09:00.000Z",
    latitude=40.78343,
    longitude=-73.96625,
)

tim_natal.julian_day = get_julian_day(tim_natal.utc_date)
