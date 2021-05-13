from typing import Tuple, Dict

from pydantic import Field

from astro.util import ZodiacSign, Polarity, Modality, Element, Point
from .base import BaseSchema


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