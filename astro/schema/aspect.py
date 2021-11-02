import math
from datetime import datetime
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


class AspectSchema(BaseSchema):
    """
    Represents information about the aspect between two points.
    """

    def __str__(self):
        if self.orb is None:
            return ""

        orb_string = f'[{round(self.orb, 4)} Orb]'
        aspect_string = f'{self.movement} {self.type}'

        if self.local_date_of_exact:
            return f'{aspect_string} {orb_string} [Exact {self.local_date_of_exact}]'
        else:
            return f'{aspect_string} {orb_string}'

    type: Optional[AspectType] = Field(
        None,
        title="Aspect Type",
        description="The type of aspect between the two points."
    )
    angle: Optional[float] = Field(
        None,
        title="Aspect Angle",
        description="The exact degrees of the angle between points."
    )
    orb: Optional[float] = Field(
        None,
        title="Aspect Orb",
        description="The current orb in degrees of the aspect."
    )
    movement: Optional[AspectMovementType] = Field(
        None,
        title="Aspect Movement",
        description="Whether the aspect is applying or separating."
    )
    days_until_exact: Optional[float] = Field(
        None,
        title="Degree Aspect Approximate Days Until Exact",
        description="The approximate amount of days until this aspect goes exact, if less than a week."
    )
    utc_date_of_exact: Optional[datetime] = Field(
        None,
        title="Degree Aspect Approximate Exact Date (UTC)",
        description="The approximate UTC date aspect goes exact, if in less than a week."
    )
    local_date_of_exact: Optional[datetime] = Field(
        None,
        title="Degree Aspect Approximate Exact Date (Local)",
        description="The approximate local date aspect goes exact, if in less than a week."
    )


class RelationshipSchema(BaseSchema):
    """
    Represents information about the relationship between two points.
    """

    def __str__(self):
        aspects = []

        if self.ecliptic_aspect.type:
            aspects.append(f'{self.ecliptic_aspect}')
        if self.declination_aspect.type:
            aspects.append(f'{self.declination_aspect}')
        if len(aspects) == 0:
            aspects.append(f'({round(self.arc_ordered, 4)}) Whole Sign {self.sign_aspect}')

        return f'From {self.from_point} to {self.to_point}: {", ".join(aspects)}'

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
    declination_arc: Optional[float] = Field(
        None,
        title="Declination Degrees Arc",
        description="The degrees between the two points relative to their declination from the equator."
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

    ecliptic_aspect: AspectSchema = Field(
        AspectSchema(),
        title="Ecliptic Aspect",
        description="The aspect between the two points based on ecliptic longitude."
    )
    declination_aspect: AspectSchema = Field(
        AspectSchema(),
        title="Declination Aspect",
        description="The aspect between the two points based on declination."
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
