from typing import Tuple, Dict, Optional, List

from pydantic import Field

from astro.util import ZodiacSign, Polarity, Modality, Element, Point
from .base import BaseSchema


class SignPointDivision(BaseSchema):
    """
    Defines a segment of a zodiac sign that is ruled by a planet.
    """
    ruler: Point = Field(
        ...,
        title="Ruler",
        description="The planet that rules this segment."
    )
    to_degree: int = Field(
        ...,
        title="Ending Degrees",
        description="The degrees of the current sign that this segment ends right before."
    )


class SignSubdivision(BaseSchema):
    """
    Defines a segment of a zodiac sign that corresponds to another zodiac sign.
    """
    sign: ZodiacSign = Field(
        ...,
        title="Zodiac Sign",
        description="The sign associated with this segment."
    )
    to_degree: float = Field(
        ...,
        title="Ending Degrees",
        description="The degrees of the current sign that this segment ends right before."
    )


class DegreeDivision(BaseSchema):
    """
    Defines a degree of a zodiac sign.
    """
    sign: ZodiacSign = Field(
        ...,
        title="Zodiac Sign",
        description="The sign associated with this segment."
    )
    sabian_symbol: str = Field(
        ...,
        title="Sabian Symbol",
        description="The sabian symbol associated with this segment."
    )


class ZodiacSignTraits(BaseSchema):
    """
    Defines traits about a specific zodiac sign.
    """
    sign: ZodiacSign = Field(
        ...,
        title="Zodiac Sign",
        description="The zodiac sign name."
    )
    polarity: Polarity = Field(
        ...,
        title="Polarity",
        description="Whether the sign is Yin or Yang."
    )
    modality: Modality = Field(
        ...,
        title="Modality",
        description="Whether the sign is cardinal, fixed, or mutable."
    )
    element: Element = Field(
        ...,
        title="Element",
        description="The element associated with this sign."
    )

    domicile_traditional: Point = Field(
        ...,
        title="Traditional Domicile",
        description="The traditional planet that rules this sign."
    )
    domicile_modern: Point = Field(
        ...,
        title="Modern Domicile",
        description="The modern planet that rules this sign."
    )
    domicile_asteroid: List[Point] = Field(
        [],
        title="Asteroid Domiciles",
        description="The asteroids that rule this sign."
    )
    exaltation: Optional[Point] = Field(
        None,
        title="Exaltation",
        description="The planet exalted in this sign."
    )
    detriment: Optional[Point] = Field(
        None,
        title="Detriment (Adversity)",
        description="The planet in detriment in this sign."
    )
    fall: Optional[Point] = Field(
        None,
        title="Fall (Depression)",
        description="The planet at fall in this sign."
    )

    triplicity: Tuple[Point, Point, Point] = Field(
        ...,
        title="Triplicity Lords",
        description="The triplicity rulers of this element, according to sect."
    )
    decans: Tuple[SignPointDivision, SignPointDivision, SignPointDivision] = Field(
        ...,
        title="Decans (Faces)",
        description="The traditional planetary rulers of the decans."
    )
    bounds: Tuple[
        SignPointDivision, SignPointDivision, SignPointDivision,
        SignPointDivision, SignPointDivision
    ] = Field(
        ...,
        title="Bounds (Terms)",
        description="The egyptian planetary rulers of the bounds."
    )
    twelfth_parts: Tuple[
        SignSubdivision, SignSubdivision, SignSubdivision, SignSubdivision,
        SignSubdivision, SignSubdivision, SignSubdivision, SignSubdivision,
        SignSubdivision, SignSubdivision, SignSubdivision, SignSubdivision,
    ] = Field(
        ...,
        title="12th Parts",
        description="The 12th part signs that subdivide this sign."
    )
    degrees: Tuple[
        DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision,
        DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision,
        DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision,
        DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision,
        DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision,
        DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision, DegreeDivision,
    ] = Field(
        ...,
        title="Degrees",
        description="The signs and symbols for each degree of this sign."
    )


class ZodiacSignCollection(BaseSchema):
    """
    A collection of all 12 zodiac signs.
    """
    signs: Dict[ZodiacSign, ZodiacSignTraits] = Field(
        ...,
        title="Zodiac Signs",
        description="The 12 Zodiac Signs.",
    )
