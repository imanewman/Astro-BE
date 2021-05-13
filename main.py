from fastapi import FastAPI

from astro.schema import ZodiacSignCollection, PointTraitsCollection, Chart, ChartSettings
from astro.util import zodiacSignTraits, pointTraits
from astro import create_chart

app = FastAPI()


@app.get("/signs")
async def get_signs() -> ZodiacSignCollection:
    """
    Calculates the default settings for the current time.

    :return: Calculated points and aspects.
    """

    return zodiacSignTraits


@app.get("/points")
async def get_points() -> PointTraitsCollection:
    """
    Calculates the default settings for the current time.

    :return: Calculated points and aspects.
    """

    return pointTraits


@app.get("/")
async def calc_now() -> Chart:
    """
    Calculates the default settings for the current time.

    :return: Calculated points and aspects.
    """

    return await calc_chart(ChartSettings())


@app.post("/chart")
async def calc_chart(settings: ChartSettings) -> Chart:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    return create_chart(settings)
