from typing import Optional, List

from pydantic import Field

from astro.util.enums import ZodiacSign, Point, SectPlacement
from .base import BaseSchema


class PointConditionSchema(BaseSchema):
    """
    Defines the bonification and maltreatment of a planet.
    For points that arent planets, all values are false.
    """

    in_joy: bool = Field(
        False,
        title="In Joy",
        description="Whether a planet is in its joy"
    )

    in_domicile: bool = Field(
        False,
        title="In Domicile",
        description="Whether a planet is in its domicile"
    )
    in_exaltation: bool = Field(
        False,
        title="In Exaltation",
        description="Whether a planet is in its exaltation"
    )
    in_triplicity: Optional[int] = Field(
        None,
        title="Triplicity Ruler Order",
        description="If it is in its triplicity, the order of triplicity importance between 1 and 3"
    )
    in_bound: bool = Field(
        False,
        title="Is Bound Ruler",
        description="Whether a planet is in its bound"
    )
    in_decan: bool = Field(
        False,
        title="Is Decan Ruler",
        description="Whether a planet is in its decan"
    )

    in_detriment: bool = Field(
        False,
        title="In Detriment",
        description="Whether a planet is in its detriment"
    )
    in_fall: bool = Field(
        False,
        title="In Fall",
        description="Whether a planet is in its fall"
    )

    sect_placement: Optional[SectPlacement] = Field(
        None,
        title="Sect Placement",
        description="Properties about this planet determined by sect"
    )

    is_under_beams: bool = Field(
        False,
        title="Is Under The Beams",
        description="Whether the planet is under the beams of the sun"
    )
    is_combust: bool = Field(
        False,
        title="Is Combust",
        description="Whether the planet is combust the sun"
    )
    is_cazimi: bool = Field(
        False,
        title="Is Cazimi",
        description="Whether the planet is cazimi the sun"
    )


class PointRulersSchema(BaseSchema):
    """
    Defines the traditional rulers of the segment of the chart this point falls in.
    """

    sign: Point = Field(
        Point.moon,
        title="Sign Ruler",
        description="The traditional planet that rules this sign",
    )
    decan: Point = Field(
        Point.moon,
        title="Decan Ruler",
        description="The traditional planet that rules this decan",
    )
    bound: Point = Field(
        Point.moon,
        title="Bound Ruler",
        description="The traditional planet that rules this bound",
    )
    triplicity: List[Point] = Field(
        [],
        title="Triplicity Ruler",
        description="The traditional planets that rule this sign in the order of importance",
    )


class PointSchema(BaseSchema):
    """
    Defines any planetary body's position relative to Earth.
    """

    name: Point = Field(
        ...,
        title="Planet or Point",
        description="The name of the planet or point"
    )

    degrees_from_aries: float = Field(
        ...,
        title="Degrees from 0 Aries",
        description="The degrees that this point is located at along the ecliptic",
        ge=0,
        lt=360
    )
    sign: ZodiacSign = Field(
        ZodiacSign.aries,
        title="Zodiac Sign",
        description="The zodiac sign this point is located within"
    )
    degrees_in_sign: int = Field(
        0,
        title="Degrees of current sign",
        description="The degrees, out of 30, that this point is located at within a sign"
    )
    minutes_in_degree: int = Field(
        0,
        title="Minutes of current degree",
        description="The minutes, out of 60, within a degree that this point is located at"
    )
    declination: Optional[float] = Field(
        None,
        title="Declination",
        description="The latitude of the point"
    )

    house: Optional[int] = Field(
        None,
        title="House",
        description="The house that this planet is in, relative to the ascendant",
        ge=1,
        le=12
    )
    ruled_houses: List[int] = Field(
        [],
        title="Ruled Houses",
        description="The houses that this planet rules"
    )

    speed: Optional[float] = Field(
        None,
        title="Longitude Degrees Moved Per Day",
        description="The degrees along the ecliptic that this point is moving per day"
    )
    declination_speed: Optional[float] = Field(
        None,
        title="Declination Degrees Moved Per Day",
        description="The degrees from the equatorial that this point is moving per day"
    )
    is_stationary: Optional[bool] = Field(
        None,
        title="Is Stationary",
        description="Whether this point is stationary on the ecliptic"
    )
    is_retrograde: Optional[bool] = Field(
        None,
        title="Is Retrograde",
        description="Whether this point is retrograde on the ecliptic"
    )

    rulers: PointRulersSchema = Field(
        PointRulersSchema(),
        title="Point Rulers",
        description="The rulers of the segment of the chart this point falls in"
    )
    condition: PointConditionSchema = Field(
        PointConditionSchema(),
        title="Condition",
        description="The state of bonification and maltreatment if this is a planet"
    )
