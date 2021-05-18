from typing import Dict, List, Optional

from pydantic import Field

from .base import BaseSchema
from ..util import AspectType, Point


class AspectTraits(BaseSchema):
    """
    Defines the traits of different types of aspects.
    """
    name: str = Field(
        ...,
        title="Aspect Name",
        description="The name of this aspect"
    )
    degrees: int = Field(
        None,
        title="Aspect Degrees",
        description="The degrees of this aspect"
    )


class AspectOrbs(BaseSchema):
    """
    Defines the orbs used for degree based aspects.
    """

    conjunction: float = Field(
        8,
        title="Conjunction",
        description="Orb of conjunction"
    )
    opposition: float = Field(
        8,
        title="Opposition",
        description="Orb of opposition"
    )
    square: float = Field(
        7,
        title="Square",
        description="Orb of square"
    )
    trine: float = Field(
        8,
        title="Trine",
        description="Orb of trine"
    )
    sextile: float = Field(
        6,
        title="Sextile",
        description="Orb of sextile"
    )

    quintile: float = Field(
        1,
        title="Quintile",
        description="Orb of quintile"
    )
    septile: float = Field(
        1,
        title="Septile",
        description="Orb of septile"
    )
    octile: float = Field(
        1,
        title="Octile",
        description="Orb of octile"
    )
    novile: float = Field(
        1,
        title="Novile",
        description="Orb of novile"
    )
    semi_sextile: float = Field(
        1,
        title="Semi-Sextile",
        description="Orb of semi-sextile"
    )
    quincunx: float = Field(
        5,
        title="Quincunx",
        description="Orb of quincunx"
    )
    sesquiquadrate: float = Field(
        1,
        title="Sesquiquadrate",
        description="Orb of sesquiquadrate"
    )
    bi_quintile: float = Field(
        1,
        title="Bi-Quintile",
        description="Orb of bi-quintile"
    )

    parallel: float = Field(
        1,
        title="Declination Parallel",
        description="Orb of parallel declination"
    )
    contraparallel: float = Field(
        1,
        title="Declination Contraparallel",
        description="Orb of contraparallel declination"
    )


class AspectTraitsCollection(BaseSchema):
    """
    A collection of all points available to use.
    """

    aspects: Dict[AspectType, AspectTraits] = Field(
        ...,
        title="Aspects",
        description="A collection of all aspects by degree",
    )
    default_orbs: AspectOrbs = Field(
        AspectOrbs(),
        title="Default Aspect Orbs",
        description="The default orbs used for each aspect"
    )


class AspectInTime(BaseSchema):
    """
    Represents information about an aspect calculated within a chart.
    """

    type: AspectType = Field(
        ...,
        title="Aspect Type",
        description="The type of aspect"
    )
    from_point: Point = Field(
        ...,
        title="From Point",
        description="The point this aspect is from"
    )
    to_point: Point = Field(
        ...,
        title="To Point",
        description="The point this aspect is to"
    )
    orb: Optional[float] = Field(
        None,
        title="Aspect Orb",
        description="The orb of this aspect"
    )


class CalculatedAspects(BaseSchema):
    """
    A collection of aspects calculated within a chart.
    """

    by_degree: List[AspectInTime] = Field(
        [],
        title="Aspects By Degree",
        description="All aspects calculated by degree"
    )
    by_sign_not_degree: List[AspectInTime] = Field(
        [],
        title="Aspects By Sign",
        description="All aspects calculated by sign that arent exact by degree"
    )
    by_declination: List[AspectInTime] = Field(
        [],
        title="Aspects By Declination",
        description="All aspects calculated by declination"
    )
