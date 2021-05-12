from datetime import datetime
from typing import List, Tuple, Dict, Optional

from humps import camelize
from pydantic import BaseModel, Field

from src.enums import *


class BaseSchema(BaseModel):
    """
    A base schema that all models inherit configuration from.
    """

    class Config:
        # CamelCase to snake_case translation automatically for every field
        alias_generator = camelize
        # Create the Pydantic models normally from python with snake_case
        allow_population_by_field_name = True
        # Strip extra whitespace around strings
        anystr_strip_whitespace = True
        # Try to access attributes by dot notation
        orm_mode = True
        # Make private attributes that won’t show up in the docs
        underscore_attrs_are_private = True
        # Gives you strings instead of the Enum class if you use enums anywhere
        use_enum_values = True


class ZodiacSignTraits(BaseSchema):
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


class ZodiacSignCollection(BaseSchema):
    """
    A collection of all 12 zodiac signs.
    """

    signs: Dict[ZodiacSign, ZodiacSignTraits] = Field(
        ...,
        title="Zodiac Signs",
        description="The 12 Zodiac Signs",
    )


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


class DateTimeLocation(BaseSchema):
    """
    Defines a time and a day at a geographic location.
    """

    date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Date",
        description="The UTC date to use, defaulting to now"
    )
    latitude: float = Field(
        36.0544,
        title="Location Latitude",
        description="The latitude of the location, defaulting to Grand Canyon, AZ"
    )
    longitude: float = Field(
        -112.1401,
        title="Location Longitude",
        description="The longitude of the location, defaulting to Grand Canyon, AZ"
    )


class CalculationSettings(BaseSchema):
    """
    Defines the input parameters for running a calculation.
    """

    start: DateTimeLocation = Field(
        DateTimeLocation(),
        title="Start Time and Location",
        description="The base date, time, and location of calculations"
    )


class ChartSummary(BaseSchema):
    """
    Summarizes the most important details of a generated chart.
    """

    sun: ZodiacSign = Field(
        ...,
        title="Sun Sign",
        description="The current zodiac sign of the sun"
    )
    moon: ZodiacSign = Field(
        ...,
        title="Moon Sign",
        description="The current zodiac sign of the moon"
    )
    asc: ZodiacSign = Field(
        ...,
        title="Ascendant Sign",
        description="The current zodiac sign of the ascendant"
    )
    asc_ruler: Point = Field(
        ...,
        title="Ascendant Ruler",
        description="The ruling planet of the ascendant"
    )
    is_day_time: bool = Field(
        ...,
        title="Is Day Time",
        description="Whether the current time is during the day"
    )


class CalculationResults(BaseSchema):
    """
    Defines the results returned after running a calculation.
    """

    start: DateTimeLocation = Field(
        ...,
        title="Start Time and Location",
        description="The base date, time, and location of calculations"
    )
    summary: Optional[ChartSummary] = Field(
        None,
        title="Chart Summary",
        description="Summarizes the most important information in a chart"
    )
    start_points: Dict[Point, PointInTime] = Field(
        [],
        title="Planets and Points",
        description="A map of the base planets and points calculated"
    )
