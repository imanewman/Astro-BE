from typing import List, Dict

from fastapi import FastAPI

from astro.schema import ZodiacSignCollection, SettingsSchema, \
    PointTraitsCollection, AspectTraitsCollection, RelationshipSchema, EventSettingsSchema
from astro.collection import aspectTraits, point_traits, zodiac_sign_traits
from astro.util import default_midpoints, default_enabled_aspects, hard_major_aspects
from astro.util.test_events import tim_natal, local_event
from astro import create_chart, ChartCollectionSchema

app = FastAPI()


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
    return aspectTraits


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
        events=[local_event]
    ))


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
                {"points": [], "midpoints": enabled_midpoints, "aspects": hard_major_aspects},
                {**event.enabled[0].dict(), "aspects": default_enabled_aspects},
            ]
        }

    return await calc_chart(SettingsSchema(
        events=[
            create_event(local_event),
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
async def calc_tim_upcoming_minimal(midpoints: bool = False) -> Dict[str, str]:
    """
    Calculates the natal chart of tim with current transits.
    Returns ordered upcoming aspects concisely.

    :param midpoints: Whether midpoints should be calculated.

    :return: Calculated aspects.
    """
    descriptions = {}
    current_date = ""

    for aspect in await calc_tim_upcoming(midpoints):
        aspect_descriptions = aspect.get_applying_aspect_descriptions()
        aspect_date = aspect_descriptions[0].split("[")[1].split(" ")[0]

        if aspect_date != current_date:
            current_date = aspect_date

            descriptions[aspect_date] = aspect_date

        for description in aspect_descriptions:
            timestamp, aspect = description.split(" | ")

            if timestamp in descriptions:
                descriptions[timestamp] += f"; {aspect}"
            else:
                descriptions[timestamp] = aspect

    return descriptions
