from typing import Tuple, Dict, Optional

from pydantic import Field

from astro.util import ZodiacSign, Polarity, Modality, Element, Point
from .base import BaseSchema


class SignDivision(BaseSchema):
    """
    Defines a segment of a zodiac sign that is ruled by a planet.
    """

    ruler: Point = Field(
        ...,
        title="Ruler",
        description="The planet that rules this division"
    )
    from_degree: int = Field(
        ...,
        title="Starting Degrees",
        description="The degrees of the current sign that this division begins at"
    )
    to_degree: int = Field(
        ...,
        title="Ending Degrees",
        description="The degrees of the current sign that this division ends right before"
    )


class ZodiacSignTraits(BaseSchema):
    """
    Defines traits about a specific zodiac sign.
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
        title="Rulership (Domicile)",
        description="The planet that rules this sign"
    )
    exaltation: Optional[Point] = Field(
        None,
        title="Exaltation",
        description="The planet exalted in this sign"
    )

    triplicity: Tuple[Point, Point, Point] = Field(
        ...,
        title="Triplicity Lords",
        description="The traditional planetary rulers of the decans in order for day, time, with the first two "
                    "elements switched at night"
    )
    bounds: Tuple[SignDivision, SignDivision, SignDivision, SignDivision, SignDivision] = Field(
        ...,
        title="Bounds (Terms)",
        description="The egyptian planetary rulers of the bounds"
    )
    decans: Tuple[SignDivision, SignDivision, SignDivision] = Field(
        ...,
        title="Decans (Faces)",
        description="The traditional planetary rulers of the decans"
    )

    detriment: Optional[Point] = Field(
        None,
        title="Detriment (Adversity)",
        description="The planet in detriment in this sign"
    )
    fall: Optional[Point] = Field(
        None,
        title="Fall (Depression)",
        description="The planet at fall in this sign"
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
