from typing import List, Dict
from functools import reduce

from fastapi import FastAPI

from astro.schema import ZodiacSignCollection, SettingsSchema, \
    PointTraitsCollection, AspectTraitsCollection, RelationshipSchema
from astro.collection import aspectTraits, point_traits, zodiac_sign_traits
from astro.util import modern_midpoints
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
    enabled_midpoints = modern_midpoints if midpoints else []
    print(midpoints)

    return await calc_chart(SettingsSchema(
        events=[
            {**tim_natal.dict(), "enabled_midpoints": enabled_midpoints},
            {**local_event.dict(), "enabled_midpoints": enabled_midpoints},
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

    def sort_aspect(relationship: RelationshipSchema) -> float:
        return min(map(
            lambda aspect: abs(aspect.days_until_exact or 7),
            relationship.get_applying_aspects()
        ), default=7)

    def filter_aspect(relationship: RelationshipSchema) -> bool:
        return len(relationship.get_applying_aspect_descriptions()) > 0

    aspects.sort(key=sort_aspect)

    return list(filter(filter_aspect, aspects))


@app.get("/tim/upcoming-min")
async def calc_tim_upcoming_minimal(midpoints: bool = False) -> Dict[str, List[str]]:
    """
    Calculates the natal chart of tim with current transits.
    Returns ordered upcoming aspects concisely.

    :param midpoints: Whether midpoints should be calculated.

    :return: Calculated aspects.
    """
    return reduce(
        lambda acc, cur: {**acc, **cur},
        map(
            lambda aspect: {aspect.get_aspect_name(): aspect.get_applying_aspect_descriptions()},
            await calc_tim_upcoming(midpoints)
        ),
        {}
    )
