from fastapi import FastAPI
import swisseph as swe

from src.globals import pointTraits
from src.models import PointInTime


app = FastAPI()


@app.get("/")
async def root():
    day = swe.julday(2021, 5, 10)
    res = {}

    for point, traits in pointTraits.points.items():
        res[point.name] = PointInTime(
            name=traits.name,
            degrees_from_aries=swe.calc_ut(day, traits.swe_id)[0][0]
        )

    return res
