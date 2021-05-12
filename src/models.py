from datetime import datetime
from typing import List, Tuple, Dict, Optional

from pydantic import BaseModel, Field

from src.enums import *


class ZodiacSignTraits(BaseModel):
    """
    Defines traits about a specific zodiac sign
    """

    sign: ZodiacSign = Field(
        ...,
        title="Zodiac Sign",
        description="The zodiac sign name"
    )
    polarity: Polarity = Field(
        ...,
        title="Polarity",
        description="Whether the sign is Yang (Masculine, Active) or Yin (Feminine, Passive)"
    )
    modality: Modality = Field(
        ...,
        title="Modality",
        description="Whether the sign is cardinal, fixed, or mutable"
    )
    element: Element = Field(
        ...,
        title="Element",
        description="The element associated with this sign"
    )
    rulership: Point = Field(
        ...,
        title="Planetary Ruler",
        description="The traditional planet that rules this sign"
    )
    decans: Tuple[Point, Point, Point] = Field(
        ...,
        title="Decans",
        description="The traditional planetary rulers of the decans, based on the chaldean order"
    )


class ZodiacSignCollection(BaseModel):
    """
    A collection of all 12 zodiac signs.
    """

    signs: Dict[ZodiacSign, ZodiacSignTraits] = Field(
        ...,
        title="Zodiac Signs",
        description="The 12 Zodiac Signs",
    )


class PointTraits(BaseModel):
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
        ...,
        title="Domicile",
        description="The signs this planet is at home in"
    )
    exaltation: List[ZodiacSign] = Field(
        ...,
        title="Exalted",
        description="The signs this planet is exalted in"
    )
    detriment: List[ZodiacSign] = Field(
        ...,
        title="Detriment",
        description="The signs this planet is in detriment in"
    )
    fall: List[ZodiacSign] = Field(
        ...,
        title="Fall",
        description="The signs this planet is in fall in"
    )


class PointTraitsCollection(BaseModel):
    """
    A collection of all points available to use.
    """

    points: Dict[Point, PointTraits] = Field(
        ...,
        title="Planets and Points",
        description="A collection of all points available to use",
    )


class PointInTime(BaseModel):
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
    declination: Optional[float] = Field(
        None,
        title="Declination",
        description="The latitude of the point"
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
    house: Optional[int] = Field(
        None,
        title="House",
        description="The house that this planet is in, relative to the ascendant",
        ge=1,
        le=12
    )


class CalculationSettings(BaseModel):
    """
    Defines the input parameters for running a calculation.
    """

    startDate: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Start Date",
        description="The UTC date of calculations, defaulting to now"
    )
    latitude: float = Field(
        36.0544,
        title="Location Latitude",
        description="The latitude of the location of calculations"
    )
    longitude: float = Field(
        -112.1401,
        title="Location Longitude",
        description="The longitude of the location of calculations"
    )


class CalculationResults(BaseModel):
    """
    Defines the results returned after running a calculation.
    """

    startDate: datetime = Field(
        ...,
        title="Start Date",
        description="The UTC date of calculations"
    )
    latitude: float = Field(
        ...,
        title="Location Latitude",
        description="The latitude of the location of calculations"
    )
    longitude: float = Field(
        ...,
        title="Location Longitude",
        description="The longitude of the location of calculations"
    )

    sun: Optional[ZodiacSign] = Field(
        None,
        title="Sun Sign",
        description="The current zodiac sign of the sun"
    )
    moon: Optional[ZodiacSign] = Field(
        None,
        title="Moon Sign",
        description="The current zodiac sign of the moon"
    )
    asc: Optional[ZodiacSign] = Field(
        None,
        title="Ascendant Sign",
        description="The current zodiac sign of the ascendant"
    )

    ascRuler: Optional[Point] = Field(
        None,
        title="Ascendant Ruler",
        description="The ruling planet of the ascendant"
    )
    is_day_time: Optional[bool] = Field(
        None,
        title="Is Day Time",
        description="Whether the current time is during the day"
    )

    startPoints: List[PointInTime] = Field(
        [],
        title="Planets and Points",
        description="A list of the planets and points calculated"
    )
