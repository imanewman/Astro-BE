from typing import Dict, Optional

from pydantic import Field

from .base import BaseSchema
from ..util import AspectType, Point, PhaseType


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

    sun_under_beams_orb: float = Field(
        17,
        title="Under The Beams Orb",
        description="The orb of conjunction for a planet to be under the beams of the sun"
    )
    sun_combust_orb: float = Field(
        8,
        title="Combust Orb",
        description="The orb of conjunction for a planet to be combust by the sun"
    )
    sun_cazimi_orb: float = Field(
        17 / 60,
        title="Cazimi Orb",
        description="The orb of conjunction for a planet to be cazimi the sun"
    )

    def aspect_to_orb(self) -> Dict[AspectType, float]:
        return {
            AspectType.conjunction: self.conjunction,
            AspectType.opposition: self.opposition,
            AspectType.square: self.square,
            AspectType.trine: self.trine,
            AspectType.sextile: self.sextile,
            AspectType.quintile: self.quintile,
            AspectType.septile: self.septile,
            AspectType.octile: self.octile,
            AspectType.novile: self.novile,
            AspectType.semi_sextile: self.semi_sextile,
            AspectType.quincunx: self.quincunx,
            AspectType.sesquiquadrate: self.sesquiquadrate,
            AspectType.bi_quintile: self.bi_quintile,
        }


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


class PointRelationship(BaseSchema):
    """
    Represents information about the relationship between two points.
    """
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
    sign_aspect: Optional[AspectType] = Field(
        None,
        title="Sign Based Aspect",
        description="The type of aspect by sign between the points"
    )
    degrees_between: Optional[float] = Field(
        None,
        title="Ecliptic Degrees Between",
        description="The degrees between the two points relative to their longitude along the ecliptic"
    )
    degree_aspect: Optional[AspectType] = Field(
        None,
        title="Degree Based Aspect",
        description="The type of aspect by degree between the two points, if one exists"
    )
    degree_aspect_orb: Optional[float] = Field(
        None,
        title="Degree Aspect Orb",
        description="The orb the degree based aspect, if it exists"
    )
    phase: Optional[PhaseType] = Field(
        None,
        title="Phase",
        description="The phase of separation between these two points"
    )
    declination_between: Optional[float] = Field(
        None,
        title="Declination Degrees Between",
        description="The degrees between the two points relative to their declination from the equator"
    )
    declination_aspect: Optional[AspectType] = Field(
        None,
        title="Declination Based Aspect",
        description="The type of aspect by declination between the two points, if one exists"
    )
    declination_aspect_orb: Optional[float] = Field(
        None,
        title="Declination Aspect Orb",
        description="The orb the declination based aspect, if it exists"
    )
