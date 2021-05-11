from datetime import date

from fastapi import FastAPI
import swisseph as swe

from src.globals import pointTraits
from src.planets import create_point


app = FastAPI()

swe.set_ephe_path()


@app.get("/")
async def root():
    current = date.today()
    day = swe.julday(current.year, current.month, current.day)
    planets = {}

    for point in pointTraits.points:
        planets[point.name] = create_point(day, point)

    return {
        "date": current,
        "planets": planets
    }
