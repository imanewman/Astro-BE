from fastapi import FastAPI
import swisseph as swe


app = FastAPI()


@app.get("/")
async def root():
    day = swe.julday(2021, 5, 10)
    return {
        "Sun": swe.calc_ut(day, swe.SUN),
        "Moon": swe.calc_ut(day, swe.MOON),
        "Venus": swe.calc_ut(day, swe.VENUS),
        "Mars": swe.calc_ut(day, swe.MARS),
        "Jupiter": swe.calc_ut(day, swe.JUPITER),
        "Saturn": swe.calc_ut(day, swe.SATURN),
    }
