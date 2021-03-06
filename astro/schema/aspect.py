from datetime import datetime, timedelta
from typing import Dict, Optional

from pydantic import Field

from astro.util import AspectType, AspectMovementType, max_approximate_days
from .base import BaseSchema


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
    relative_velocity: Optional[float] = Field(
        None,
        title="Relative Velocity",
        description="The relative velocity between the two points, if they are in aspect."
    )
    movement: Optional[AspectMovementType] = Field(
        None,
        title="Aspect Movement",
        description="Whether the aspect is applying or separating."
    )

    def __str__(self):
        if self.movement and self.type and self.orb:
            return f"{self.movement} {self.type} ({self.orb})"
        else:
            return ""

    def get_approximate_timing(self) -> Optional[timedelta]:
        """
        :return: The time delta until this aspect goes exact, if it does soon.
        """
        if not self.relative_velocity or not self.orb:
            return

        approximate_days_until_exact = self.orb / self.relative_velocity

        if abs(approximate_days_until_exact) < max_approximate_days:
            return timedelta(days=approximate_days_until_exact)
