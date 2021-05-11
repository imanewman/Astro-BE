from typing import List, Tuple, Dict

from pydantic import BaseModel, Field, validator, root_validator

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
    domicile: List[Point] = Field(
        ...,
        title="Domicile",
        description="The planets at home in this sign"
    )
    exaltation: List[Point] = Field(
        ...,
        title="Exalted",
        description="The planets exalted in this sign"
    )
    detriment: List[Point] = Field(
        ...,
        title="Detriment",
        description="The planets in detriment in this sign"
    )
    fall: List[Point] = Field(
        ...,
        title="Fall",
        description="The planets at fall in this sign"
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
    is_traditional: bool = Field(
        False,
        title="Is Traditional Planet",
        description="Whether this planet is a traditional planet",
    )
    is_outer: bool = Field(
        False,
        title="Is Outer Planet",
        description="Whether this planet is an outer planet",
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

    @root_validator()
    def set_sign_and_degrees(cls, values):
        degrees_from_aries = values.get("degrees_from_aries")

        values.update({
            "sign": [
                ZodiacSign.aries,
                ZodiacSign.taurus,
                ZodiacSign.gemini,
                ZodiacSign.cancer,
                ZodiacSign.leo,
                ZodiacSign.virgo,
                ZodiacSign.libra,
                ZodiacSign.scorpio,
                ZodiacSign.sagittarius,
                ZodiacSign.capricorn,
                ZodiacSign.aquarius,
                ZodiacSign.pisces
            ][int(degrees_from_aries / 30)],
            "degrees_in_sign": int(degrees_from_aries % 30),
            "minutes_in_degree": int(degrees_from_aries % 1 * 60),
        })

        return values

