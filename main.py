from fastapi import FastAPI

from astro.schema import ZodiacSignCollection, ChartSchema, SettingsSchema, \
    PointTraitsCollection, AspectTraitsCollection, EventSchema, EventSettingsSchema
from astro.collection import aspectTraits
from astro.collection.point_traits import point_traits
from astro.collection.zodiac_sign_traits import zodiac_sign_traits
from astro.util.tim import tim_natal, local_event
from astro import create_chart, ChartCollectionSchema

app = FastAPI()


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


@app.post("/chart")
async def calc_chart(settings: SettingsSchema) -> ChartCollectionSchema:
    """
    Calculates the chart for a given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    return create_chart(settings)


@app.get("/")
async def calc_now() -> ChartCollectionSchema:
    """
    Calculates the chart for the current time.

    :return: Calculated points and aspects.
    """

    return await calc_chart(SettingsSchema(
        events=[EventSettingsSchema()]
    ))


@app.get("/local")
async def calc_local() -> ChartCollectionSchema:
    """
    Calculates the current chart in the current location.

    :return: Calculated points and aspects.
    """

    return await calc_chart(SettingsSchema(
        events=[local_event]
    ))


@app.get("/tim")
async def calc_tim() -> ChartCollectionSchema:
    """
    Calculates the natal chart of tim.

    :return: Calculated points and aspects.
    """
    return await calc_chart(SettingsSchema(
        events=[tim_natal]
    ))


@app.get("/tim/transits")
async def calc_tim_transits() -> ChartCollectionSchema:
    """
    Calculates the natal chart of tim with current transits.

    :return: Calculated points and aspects.
    """
    return await calc_chart(SettingsSchema(
        events=[tim_natal, local_event]
    ))
