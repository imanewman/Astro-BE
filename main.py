import re
from datetime import timedelta, datetime
from typing import List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from astro.schema import ZodiacSignCollection, SettingsSchema, \
    PointTraitsCollection, AspectTraitsCollection, RelationshipSchema, EventSettingsSchema, TransitSchema
from astro.collection import aspect_traits, point_traits, zodiac_sign_traits
from astro.schema.timezone import TimezoneSchema, TimezoneQuerySchema
from astro.timezone import calculate_timezone
from astro.util import default_midpoints, AspectType
from astro.util.test_events import tim_natal, local_event, tim_transits
from astro import create_chart, ChartCollectionSchema, create_points_with_attributes, calculate_relationships

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static Collections


@app.get("/signs")
async def get_signs() -> ZodiacSignCollection:
    """
    Returns information about each zodiac sign.

    :return: The zodiac signs.
    """
    return zodiac_sign_traits


@app.get("/points")
async def get_points() -> PointTraitsCollection:
    """
    Returns information about each planet and point.

    :return: The points.
    """
    return point_traits


@app.get("/aspects")
async def get_aspects() -> AspectTraitsCollection:
    """
    Returns information about each degree aspect between points.

    :return: The zodiac signs.
    """
    return aspect_traits


@app.get("/timezone")
async def calc_timezone() -> TimezoneSchema:
    """
    Returns the calculated geolocation, timezone, and UTC date for a location name and date.

    :return: The calculated timezone
    """
    return calculate_timezone(
        TimezoneQuerySchema(
            location_name="Manhattan, NY",
            local_date="1997-10-11T11:09:00.000Z"
        )
    )


# Chart Calculations


@app.post("/chart")
async def calc_chart(settings: SettingsSchema) -> ChartCollectionSchema:
    """
    Calculates the chart for a given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """
    return create_chart(settings)


@app.get("/now")
async def calc_now() -> ChartCollectionSchema:
    """
    Calculates the current chart in the current location.

    :return: Calculated points and aspects.
    """
    return await calc_chart(SettingsSchema(
        events=[local_event()]
    ))


@app.post("/timezone")
async def calc_timezone(query: TimezoneQuerySchema) -> TimezoneSchema:
    """
    Returns the calculated geolocation, timezone, and UTC date for a location name and date.

    :return: The calculated timezone
    """
    return calculate_timezone(query)


# Tim Test Endpoints


@app.get("/tim")
async def calc_tim() -> ChartCollectionSchema:
    """
    Calculates the natal chart of tim.

    :return: Calculated points and aspects.
    """
    return await calc_chart(SettingsSchema(
        events=[tim_natal],
    ))


@app.get("/tim/transits/chart")
async def calc_tim_transits_chart(midpoints: bool = False) -> ChartCollectionSchema:
    """
    Calculates the natal chart of tim with current transits.

    :param midpoints: Whether midpoints should be calculated.

    :return: Calculated points and aspects.
    """
    enabled_midpoints = default_midpoints if midpoints else []

    def create_event(event: EventSettingsSchema):
        return {
            **event.dict(),
            "enabled": [
                *event.enabled,
                {
                    "points": [],
                    "midpoints": enabled_midpoints,
                    "aspects": [
                        AspectType.conjunction,
                        AspectType.opposition,
                    ]
                },
            ]
        }

    return await calc_chart(SettingsSchema(
        events=[
            create_event(local_event()),
            create_event(tim_natal)
        ]
    ))


@app.get("/tim/transits/upcoming")
async def calc_tim_transits_upcoming() -> List[TransitSchema]:
    """
    Generates upcoming transits.

    :return: The calculated transits.
    """
    calculated = await calc_chart(SettingsSchema(
        events=[tim_transits]
    ))

    return calculated.charts[0].transits


@app.get("/tim/transits/min")
async def calc_tim_transits_min() -> Dict[str, Dict[str, str]]:
    """
    Generates upcoming transits.

    :return: The calculated transits.
    """
    descriptions_by_timestamp = {}
    descriptions_by_day = {}

    for transit in await calc_tim_transits_upcoming():
        timestamp = transit.get_time()

        if timestamp in descriptions_by_timestamp:
            descriptions_by_timestamp[timestamp] += f"; {transit.get_name()}"
        else:
            descriptions_by_timestamp[timestamp] = transit.get_name()

    for timestamp, aspect in descriptions_by_timestamp.items():
        day = timestamp.split(" ")[0]

        if day not in descriptions_by_day:
            descriptions_by_day[day] = {}

        descriptions_by_day[day][timestamp] = aspect

    return descriptions_by_day
