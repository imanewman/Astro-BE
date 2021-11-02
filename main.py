from typing import List

from fastapi import FastAPI

from astro.schema import ZodiacSignCollection, SettingsSchema, \
    PointTraitsCollection, AspectTraitsCollection, EventSettingsSchema, RelationshipSchema
from astro.collection import aspectTraits
from astro.collection.point_traits import point_traits
from astro.collection.zodiac_sign_traits import zodiac_sign_traits
from astro.util import AspectMovementType
from astro.util.tim import tim_natal, local_event
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
    Calculates the chart for the current time.

    :return: Calculated points and aspects.
    """

    return await calc_chart(SettingsSchema(
        events=[EventSettingsSchema()]
    ))


@app.get("/now-local")
async def calc_local() -> ChartCollectionSchema:
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


@app.get("/tim/upcoming")
async def calc_tim_upcoming() -> List[RelationshipSchema]:
    """
    Calculates the natal chart of tim with current transits.
    Returns ordered upcoming aspects.

    :return: Calculated aspects.
    """

    calculated_transits = await calc_tim_transits()
    aspects = calculated_transits.relationships[2].relationships
    applying_aspects = [AspectMovementType.applying, AspectMovementType.mutually_applying]

    def do_track_aspect(aspect: RelationshipSchema) -> bool:
        if aspect.ecliptic_aspect.days_until_exact is not None and \
                aspect.ecliptic_aspect.movement in applying_aspects:
            return True

        if aspect.declination_aspect.days_until_exact is not None and \
                aspect.declination_aspect.movement in applying_aspects:
            return True

        return False

    def sort_aspect(aspect: RelationshipSchema) -> float:
        ecliptic_days_until_exact = aspect.ecliptic_aspect.days_until_exact
        declination_days_until_exact = aspect.declination_aspect.days_until_exact

        if ecliptic_days_until_exact is not None and declination_days_until_exact is not None:
            return min(abs(ecliptic_days_until_exact), abs(declination_days_until_exact))
        elif ecliptic_days_until_exact is not None:
            return abs(ecliptic_days_until_exact)
        elif declination_days_until_exact is not None:
            return abs(declination_days_until_exact)

        return 7

    upcoming_aspects = list(filter(do_track_aspect, aspects))

    upcoming_aspects.sort(key=sort_aspect)

    return upcoming_aspects


@app.get("/tim/upcoming-text")
async def calc_tim_upcoming_text() -> List[str]:
    """
    Calculates the natal chart of tim with current transits.
    Returns ordered upcoming aspects in text.

    :return: Calculated aspects.
    """

    upcoming_transits = await calc_tim_upcoming()

    return list(map(lambda aspect: str(aspect), upcoming_transits))
