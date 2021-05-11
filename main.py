from datetime import datetime

from fastapi import FastAPI
import swisseph as swe

from src.globals import pointTraits
from src.planets import create_point
from src.time import get_julian_day

app = FastAPI()

swe.set_ephe_path()


@app.get("/")
async def root():
    current = datetime.utcnow()
    day = get_julian_day(current)
    planets = {}

    for point in pointTraits.points:
        planets[point.name] = create_point(day, point)

    return {
        "now": current,
        "planets": planets
    }
