import re
from datetime import timedelta, datetime
from typing import List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from astro.schema import ZodiacSignCollection, SettingsSchema, \
    PointTraitsCollection, AspectTraitsCollection, RelationshipSchema, EventSettingsSchema
from astro.collection import aspect_traits, point_traits, zodiac_sign_traits
from astro.schema.timezone import TimezoneSchema, TimezoneQuerySchema
from astro.timezone import calculate_timezone
from astro.util import default_midpoints, AspectType
from astro.util.test_events import tim_natal, local_event
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


@app.get("/tim/transits")
async def calc_tim_transits(midpoints: bool = False) -> ChartCollectionSchema:
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


@app.get("/tim/upcoming")
async def calc_tim_upcoming(midpoints: bool = False) -> List[RelationshipSchema]:
    """
    Calculates the natal chart of tim with current transits.
    Returns ordered upcoming aspects.

    :param midpoints: Whether midpoints should be calculated.

    :return: Calculated aspects.
    """
    calculated_transits = await calc_tim_transits(midpoints)
    aspects = calculated_transits.relationships[2].relationships

    return list(filter(lambda rel: rel.has_applying_aspects(), aspects))


@app.get("/tim/upcoming-min")
async def calc_tim_upcoming_minimal(midpoints: bool = False) -> Dict[str, Dict[str, str]]:
    """
    Calculates the natal chart of tim with current transits.
    Returns ordered upcoming aspects concisely.

    :param midpoints: Whether midpoints should be calculated.

    :return: Calculated aspects.
    """
    descriptions_by_timestamp = {}
    descriptions_by_day = {}

    for aspect in await calc_tim_upcoming(midpoints):
        aspect_descriptions = aspect.get_applying_aspect_descriptions()

        for description in aspect_descriptions:
            timestamp, aspect = description.split(" | ")

            if timestamp in descriptions_by_timestamp:
                descriptions_by_timestamp[timestamp] += f"; {aspect}"
            else:
                descriptions_by_timestamp[timestamp] = aspect

    for timestamp, aspect in descriptions_by_timestamp.items():
        day = timestamp.split(" ")[0][1:]
        short_timestamp = re.sub(r"\d\d\d\d-", "", timestamp)

        if day not in descriptions_by_day:
            descriptions_by_day[day] = {}

        descriptions_by_day[day][short_timestamp] = aspect

    return descriptions_by_day


@app.get("/tim/many-transits")
async def tim_transit_test() -> List[List[str]]:
    """
    Test endpoint for how long it takes to generate transits.

    :return: The calculated timezone
    """
    settings = SettingsSchema(
        events=[local_event()],
        do_calculate_point_attributes=False,
        do_calculate_relationship_attributes=False
    )
    event_settings = settings.events[0]
    increments = 7 * 24  # Transits for 1 week polling 1 hour at a time.
    all_relationships = []
    points = [point for point in create_points_with_attributes(event_settings, settings).values()]
    start_time = datetime.now()

    for increment in range(0, increments):
        event_settings.event.utc_date += timedelta(hours=1)
        transit_points = [point for point in create_points_with_attributes(event_settings, settings).values()]
        relationships = calculate_relationships(
            (points, event_settings),
            (transit_points, event_settings),
            False,
            settings
        )
        relationships_close_to_exact = list(map(
            lambda rel: f"{rel.get_aspect_name()} {rel.ecliptic_aspect}",
            filter(
                lambda rel: rel.ecliptic_aspect.orb and rel.ecliptic_aspect.orb < 0.01,
                relationships
            )
        ))

        all_relationships.append(relationships_close_to_exact)

    end_time = datetime.now()
    run_time = end_time - start_time

    print(f"Ran {increments} iterations in {run_time.seconds} seconds")

    return all_relationships


@app.get("/tim/new-transits")
async def tim_transit_new() -> ChartCollectionSchema:
    """
    Test endpoint for how long it takes to generate transits.

    :return: The calculated timezone
    """
    return await calc_chart(SettingsSchema(
            events=[{
                **tim_natal.dict(),
                "transits": {
                    "do_calculate_ecliptic": True,
                    "start_date": "2022-06-17T00:00:00.000Z",
                    "end_date": "2022-06-18T00:00:00.000Z",
                    "enabled": local_event().enabled
                }
            }]
        )
    )

