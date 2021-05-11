from fastapi import FastAPI
import swisseph as swe

from src.models import CalculationSettings, CalculationResults
from src.planets import create_all_points

app = FastAPI()

swe.set_ephe_path()


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

    :return: Calculated points and aspects.
    """

    return CalculationResults(
        **settings.dict(),
        points=create_all_points(settings)
    )
