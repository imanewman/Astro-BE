from fastapi import FastAPI

from src.globals import *
from src.models import *
from src.calculate import create_results

app = FastAPI()

swe.set_ephe_path()


@app.get("/signs")
async def root() -> ZodiacSignCollection:
    """
    Calculates the default settings for the current time.

    :return: Calculated points and aspects.
    """

    return zodiacSignTraits


@app.get("/points")
async def root() -> PointTraitsCollection:
    """
    Calculates the default settings for the current time.

    :return: Calculated points and aspects.
    """

    return pointTraits


@app.get("/")
async def root() -> CalculationResults:
    """
    Calculates the default settings for the current time.

    :return: Calculated points and aspects.
    """

    return await calc(CalculationSettings())


@app.post("/calc")
async def calc(settings: CalculationSettings) -> CalculationResults:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    return create_results(settings)
