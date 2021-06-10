import datetime

from fastapi import FastAPI

from astro.schema import ZodiacSignCollection, PointTraitsCollection, Chart, ChartSettings
from astro.schema.aspect import AspectTraitsCollection
from astro.util import zodiac_sign_traits, point_traits, aspectTraits, tim_natal
from astro import create_chart

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


@app.get("/")
async def calc_now() -> Chart:
    """
    Calculates the chart for the current time.

    :return: Calculated points and aspects.
    """

    return await calc_chart(ChartSettings())


@app.post("/chart")
async def calc_chart(settings: ChartSettings) -> Chart:
    """
    Calculates the chart for a given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    return create_chart(settings)


@app.get("/local")
async def calc_local() -> Chart:
    """
    Calculates the current chart in the current location

    :return: Calculated points and aspects.
    """

    return await calc_chart(
        ChartSettings(**{
            "start": {
                "latitude": 35.2828,
                "longitude": -120.6596
            }
        })
    )


@app.get("/tim")
async def calc_tim() -> Chart:
    """
    Calculates the natal chart of tim.

    :return: Calculated points and aspects.
    """

    return await calc_chart(ChartSettings(start=tim_natal))
