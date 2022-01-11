import math
from datetime import datetime
from typing import Dict, Optional, List, Union

from pydantic import Field

from .base import BaseSchema
from astro.util import AspectType, Point, PhaseType, AspectMovementType, applying_aspects


class AspectOrbsSchema(BaseSchema):
    """
    Defines the orbs used for aspects.
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
        5,
        title="Quintile",
        description="Orb of quintile"
    )
    bi_quintile: float = Field(
        5,
        title="Bi-Quintile",
        description="Orb of bi-quintile"
    )

    septile: float = Field(
        3,
        title="Septile",
        description="Orb of septile"
    )
    bi_septile: float = Field(
        3,
        title="Bi-Septile",
        description="Orb of bi-septile"
    )
    tri_septile: float = Field(
        3,
        title="Tri-Septile",
        description="Orb of tri-septile"
    )

    octile: float = Field(
        3,
        title="Octile",
        description="Orb of octile"
    )
    sesquiquadrate: float = Field(
        3,
        title="Sesquiquadrate",
        description="Orb of sesquiquadrate"
    )

    novile: float = Field(
        1,
        title="Novile",
        description="Orb of novile"
    )
    bi_novile: float = Field(
        1,
        title="Bi-Novile",
        description="Orb of bi-novile"
    )
    quadri_novile: float = Field(
        1,
        title="Quadri-Novile",
        description="Orb of quadri-novile"
    )

    semi_sextile: float = Field(
        1,
        title="Semi-Sextile",
        description="Orb of semi-sextile"
    )
    quincunx: float = Field(
        2,
        title="Quincunx",
        description="Orb of quincunx"
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
            AspectType.bi_quintile: self.bi_quintile,
            AspectType.septile: self.septile,
            AspectType.bi_septile: self.bi_septile,
            AspectType.tri_septile: self.tri_septile,
            AspectType.octile: self.octile,
            AspectType.sesquiquadrate: self.sesquiquadrate,
            AspectType.novile: self.novile,
            AspectType.bi_novile: self.bi_novile,
            AspectType.quadri_novile: self.quadri_novile,
            AspectType.semi_sextile: self.semi_sextile,
            AspectType.quincunx: self.quincunx,
        }


class AspectSchema(BaseSchema):
    """
    Represents information about the aspect between two points.
    """
    type: Optional[AspectType] = Field(
        None,
        title="Aspect Type",
        description="The type of aspect between the two points."
    )
    is_precession_corrected: bool = Field(
        False,
        title="Is Precession Corrected",
        description="Whether this aspect is corrected for precession between events."
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

    def __str__(self):
        if self.orb is None:
            return ""
        elif self.local_date_of_exact:
            return f"{self.get_date_stamp()} | {self.type}"
        else:
            return self.type

    def get_date_stamp(self) -> str:
        """
        :return: A small date stamp of the minute of this exact aspect.
        """
        correction = " PC" if self.is_precession_corrected else ""

        return f"[{':'.join(str(self.local_date_of_exact).split(':')[0:2])}{correction}]"


class RelationshipSchema(BaseSchema):
    """
    Represents information about the relationship between two points.
    """
    from_point: Union[Point, str] = Field(
        ...,
        title="From Point",
        description="The point this aspect is from."
    )
    to_point: Union[Point, str] = Field(
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

    precession_correction: float = Field(
        0,
        title="Precession Correction",
        description="The precession correction in degrees from the first to the second event."
    )

    ecliptic_aspect: AspectSchema = Field(
        AspectSchema(),
        title="Ecliptic Aspect",
        description="The aspect between the two points based on ecliptic longitude."
    )
    precession_corrected_aspect: AspectSchema = Field(
        AspectSchema(is_precession_corrected=True),
        title="Precession Corrected Ecliptic Aspect",
        description="The aspect between the two points based on ecliptic longitude, corrected for precession."
    )
    declination_aspect: AspectSchema = Field(
        AspectSchema(),
        title="Declination Aspect",
        description="The aspect between the two points based on declination."
    )

    def __str__(self):
        return f'{self.get_aspect_name()}: {", ".join(self.get_applying_aspect_descriptions())}'

    def get_aspect_name(self) -> str:
        return f'{self.from_point} To {self.to_point}'

    def get_applying_aspects(self) -> List[AspectSchema]:
        """
        Returns all aspects that have an upcoming approximate exact date.

        :return: A list of aspects.
        """
        aspects = [
            self.ecliptic_aspect,
            self.precession_corrected_aspect,
            self.declination_aspect
        ]

        return list(filter(
            lambda aspect: aspect.days_until_exact and aspect.movement in applying_aspects,
            aspects
        ))

    def has_applying_aspects(self) -> bool:
        """
        Returns whether any aspect has an upcoming date.

        :return: Whether any aspect is closely applying.
        """
        return len(self.get_applying_aspects()) > 0

    def get_applying_aspect_descriptions(self) -> List[str]:
        aspects_strings = []
        aspect_types = []

        for aspect in self.get_applying_aspects():
            try:
                existing_type_index = aspect_types.index(aspect.type)

                aspects_strings[existing_type_index] = \
                    aspects_strings[existing_type_index].replace("]", f"]{aspect.get_date_stamp()}")
            except ValueError:
                aspects_strings.append(f'{aspect} From {self.get_aspect_name()}')

            aspect_types.append(aspect.type)

        return aspects_strings


class RelationshipCollectionSchema(BaseSchema):
    """
    Represents the relationships between all points.
    """
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
