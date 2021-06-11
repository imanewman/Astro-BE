from typing import Optional, List, Dict

from pydantic import Field

from astro.util import PointCategory, ZodiacSign, Point, AspectType
from .base import BaseSchema
from .aspect import AspectOrbsSchema


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


class AspectTraitsCollection(BaseSchema):
    """
    A collection of all points available to use.
    """

    aspects: Dict[AspectType, AspectTraits] = Field(
        ...,
        title="Aspects",
        description="A collection of all aspects by degree",
    )
    default_orbs: AspectOrbsSchema = Field(
        AspectOrbsSchema(),
        title="Default Aspect Orbs",
        description="The default orbs used for each aspect"
    )