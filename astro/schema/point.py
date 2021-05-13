from typing import Optional, List, Dict

from pydantic import Field

from astro.util.enums import PointCategory, ZodiacSign, Point
from .base import BaseSchema


class PointTraits(BaseSchema):
    """
    Information about a specific planet or point.
    """

    swe_id: int = Field(
        ...,
        title="Swiss Ephemeris ID",
        description="The fixed number associated with this point in the swiss ephemeris",
    )
    name: str = Field(
        ...,
        title="Name",
        description="The name of this planet or point",
    )
    category: Optional[PointCategory] = Field(
        None,
        title="Point Category",
        description="The category of point this is",
    )
    joy: Optional[int] = Field(
        None,
        title="Planetary Joy House",
        description="The house that this planet is at its joy in",
        ge=1,
        le=12
    )
    domicile: List[ZodiacSign] = Field(
        [],
        title="Domicile",
        description="The signs this planet is at home in"
    )
    exaltation: List[ZodiacSign] = Field(
        [],
        title="Exalted",
        description="The signs this planet is exalted in"
    )
    detriment: List[ZodiacSign] = Field(
        [],
        title="Detriment",
        description="The signs this planet is in detriment in"
    )
    fall: List[ZodiacSign] = Field(
        [],
        title="Fall",
        description="The signs this planet is in fall in"
    )
    speed_avg: Optional[float] = Field(
        None,
        title="Average Speed",
        description="The average speed of this point, in degrees"
    )
    speed_high: Optional[float] = Field(
        None,
        title="Highest Speed",
        description="The highest speed of this point, in degrees"
    )
    speed_low: Optional[float] = Field(
        None,
        title="Lowest Speed",
        description="The lowest speed of this point, in degrees"
    )


class PointTraitsCollection(BaseSchema):
    """
    A collection of all points available to use.
    """

    points: Dict[Point, PointTraits] = Field(
        ...,
        title="Planets and Points",
        description="A collection of all points available to use",
    )


class PointInTime(BaseSchema):
    """
    Defines any planetary body's position relative to Earth.
    """

    name: Point = Field(
        ...,
        title="Planet or Point",
        description="The name of the planet or point"
    )

    degrees_from_aries: float = Field(
        ...,
        title="Degrees from 0 Aries",
        description="The degrees, out of 360, that this point is located at relative to 0 degrees Aries",
        ge=0,
        lt=360
    )
    sign: ZodiacSign = Field(
        ZodiacSign.aries,
        title="Zodiac Sign",
        description="The zodiac sign this point is located within"
    )
    degrees_in_sign: int = Field(
        0,
        title="Degrees of current sign",
        description="The degrees, out of 30, that this point is located at within a sign"
    )
    minutes_in_degree: int = Field(
        0,
        title="Minutes of current degree",
        description="The minutes (out of 60) within a degree that this point is located at"
    )
    declination: Optional[float] = Field(
        None,
        title="Declination",
        description="The latitude of the point"
    )

    house: Optional[int] = Field(
        None,
        title="House",
        description="The house that this planet is in, relative to the ascendant",
        ge=1,
        le=12
    )
    ruled_houses: List[int] = Field(
        [],
        title="Ruled Houses",
        description="The houses that this planet rules"
    )

    speed: Optional[float] = Field(
        None,
        title="Degrees Moved Per Day",
        description="The degrees that this point is moving per day"
    )
    is_stationary: Optional[bool] = Field(
        None,
        title="Is Stationary",
        description="Whether this point is stationary"
    )
    is_retrograde: Optional[bool] = Field(
        None,
        title="Is Retrograde",
        description="Whether this point is retrograde"
    )
