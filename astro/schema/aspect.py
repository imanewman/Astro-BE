import math
from typing import Dict, Optional, List

from pydantic import Field

from .base import BaseSchema
from astro.util import AspectType, Point, PhaseType, AspectMovementType


class AspectOrbsSchema(BaseSchema):
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


class RelationshipSchema(BaseSchema):
    """
    Represents information about the relationship between two points.
    """

    def __str__(self):
        aspect_between = f'from {self.from_point} to {self.to_point}'
        aspects = []

        def days_to_string(days: Optional[float]) -> str:
            if days is None:
                return ""

            return f'[{round(days * 24, 2)}H To Exact] '

        if self.degree_aspect:
            hours_until_exact_text = days_to_string(self.degree_aspect_approx_days)

            aspects.append(f'[{round(self.degree_aspect_orb, 4)} Orb] {hours_until_exact_text}' +
                           f'{self.degree_aspect_movement} {self.degree_aspect} {aspect_between}')
        if self.declination_aspect:
            hours_until_exact_text = days_to_string(self.declination_aspect_approx_days)

            aspects.append(f'[{round(self.declination_aspect_orb, 4)} Orb] {hours_until_exact_text}' +
                           f'{self.declination_aspect_movement} {self.declination_aspect} {aspect_between}')
        if len(aspects) == 0:
            aspects.append(f'({round(self.arc_ordered, 4)}) Whole Sign {self.sign_aspect} {aspect_between}')

        return ", ".join(aspects)

    from_point: Point = Field(
        ...,
        title="From Point",
        description="The point this aspect is from."
    )
    to_point: Point = Field(
        ...,
        title="To Point",
        description="The point this aspect is to."
    )

    sign_aspect: Optional[AspectType] = Field(
        None,
        title="Sign Based Aspect",
        description="The type of aspect by sign between the points."
    )

    arc_ordered: Optional[float] = Field(
        None,
        title="Ecliptic Degrees Between",
        description="The degrees between the two points relative to their longitude along the ecliptic. "
                    "This value will always be the arc from the first to the second point."
    )
    arc_minimal: Optional[float] = Field(
        None,
        title="Ecliptic Degrees Between",
        description="The arc between the two points relative to their longitude along the ecliptic. "
                    "This value will always be the smaller arc between the two points."
    )

    phase: Optional[PhaseType] = Field(
        None,
        title="Phase",
        description="The phase of separation between these two points."
    )
    phase_base_point: Optional[Point] = Field(
        None,
        title="Phase Base Point",
        description="The point being used as the base for the phase between points."
    )

    degree_aspect: Optional[AspectType] = Field(
        None,
        title="Degree Based Aspect",
        description="The type of aspect by degree between the two points."
    )
    degree_aspect_angle: Optional[float] = Field(
        None,
        title="Degree Aspect Angle",
        description="The angle degrees of the degree based aspect."
    )
    degree_aspect_orb: Optional[float] = Field(
        None,
        title="Degree Aspect Orb",
        description="The orb of the degree based aspect."
    )
    degree_aspect_movement: Optional[AspectMovementType] = Field(
        None,
        title="Degree Aspect Movement",
        description="Whether the degree aspect is applying or separating."
    )
    degree_aspect_approx_days: Optional[float] = Field(
        None,
        title="Degree Aspect Approximate Days Until Exist",
        description="The approximate amount of days until this degree aspect goes exact, if less than a week."
    )

    declination_arc: Optional[float] = Field(
        None,
        title="Declination Degrees Arc",
        description="The degrees between the two points relative to their declination from the equator."
    )
    declination_aspect: Optional[AspectType] = Field(
        None,
        title="Declination Based Aspect",
        description="The type of aspect by declination between the two points,."
    )
    declination_aspect_orb: Optional[float] = Field(
        None,
        title="Declination Aspect Orb",
        description="The orb the declination based aspect."
    )
    declination_aspect_movement: Optional[AspectMovementType] = Field(
        None,
        title="Declination Aspect Movement",
        description="Whether the declination aspect is applying or separating."
    )
    declination_aspect_approx_days: Optional[float] = Field(
        None,
        title="Declination Aspect Approximate Days Until Exist",
        description="The approximate amount of days until this declination aspect goes exact, if less than a week."
    )


class RelationshipCollectionSchema(BaseSchema):
    from_chart_index: int = Field(
        0,
        title="From Chart Index",
        description="The index of the chart that these aspects are calculated going from."
    )
    to_chart_index: Optional[int] = Field(
        None,
        title="To Chart Index",
        description="The index of the chart that these aspects are calculated going to. "
                    "The value is null if aspects are within a single chart."
    )
    relationships: List[RelationshipSchema] = Field(
        [],
        title="Relationships",
        description="A list of relationships between every set of points in the first to the second chart."
    )
