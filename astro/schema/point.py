from typing import Optional, List, Union

from pydantic import Field

from astro.util.enums import ZodiacSign, Point, SectPlacement, Modality, Element, HouseSystem, SunCondition
from .base import BaseSchema


class PointConditionSchema(BaseSchema):
    """
    Defines the bonification and maltreatment of a planet.
    For points that arent planets, all values are false.
    """
    in_joy: bool = Field(
        False,
        title="In Joy",
        description="Whether a planet is in its joy."
    )

    in_domicile: bool = Field(
        False,
        title="In Domicile",
        description="Whether a planet is in its domicile."
    )
    in_exaltation: bool = Field(
        False,
        title="In Exaltation",
        description="Whether a planet is in its exaltation."
    )
    in_detriment: bool = Field(
        False,
        title="In Detriment",
        description="Whether a planet is in its detriment."
    )
    in_fall: bool = Field(
        False,
        title="In Fall",
        description="Whether a planet is in its fall."
    )

    in_triplicity: Optional[int] = Field(
        None,
        title="Triplicity Ruler Order",
        description="If it is in its triplicity, the order of triplicity importance between 1 and 3."
    )
    in_bound: bool = Field(
        False,
        title="Is Bound Ruler",
        description="Whether a planet is in its own bound."
    )
    in_decan: bool = Field(
        False,
        title="Is Decan Ruler",
        description="Whether a planet is in its own decan."
    )

    sect_placement: Optional[SectPlacement] = Field(
        None,
        title="Sect Placement",
        description="Properties of this planet determined by sect."
    )

    sun_proximity: Optional[SunCondition] = Field(
        None,
        title="Sun Proximity",
        description="Whether the planet is under the beams of, combust, or cazimi sun."
    )


class PointRulersSchema(BaseSchema):
    """
    Defines the traditional rulers of the segment of the chart this point falls in.
    """
    sign: Optional[Point] = Field(
        None,
        title="Sign Ruler",
        description="The traditional planet that rules this sign.",
    )
    decan: Optional[Point] = Field(
        None,
        title="Decan Ruler",
        description="The traditional planet that rules this decan.",
    )
    bound: Optional[Point] = Field(
        None,
        title="Bound Ruler",
        description="The traditional planet that rules this bound.",
    )
    triplicity: List[Point] = Field(
        [],
        title="Triplicity Ruler",
        description="The traditional planets that rule this element in the order of importance.",
    )


class PointHousesSchema(BaseSchema):
    """
    Defines the house and ruled houses of a point for a given house system.
    """
    house_system: HouseSystem = Field(
        HouseSystem.whole_sign,
        title="House System",
        description="The house system used.",
    )
    house: Optional[int] = Field(
        None,
        title="House",
        description="The house that this planet is in.",
        ge=1,
        le=12
    )
    ruled_houses: List[int] = Field(
        [],
        title="Ruled Houses",
        description="The houses that this planet rules."
    )


class PointSchema(BaseSchema):
    """
    Defines any planetary body's position relative to Earth.
    """
    name: Union[Point, str] = Field(
        ...,
        title="Planet or Point",
        description="The name of the planet or point."
    )
    points: List[Point] = Field(
        ...,
        title="Points",
        description="THe points composited to create this point."
    )

    longitude: float = Field(
        ...,
        title="Ecliptic Longitude",
        description="The degrees of longitude of this point along the ecliptic.",
        ge=0,
        lt=360
    )
    longitude_velocity: Optional[float] = Field(
        None,
        title="Longitude Degrees Moved Per Day",
        description="The degrees along the ecliptic that this point is moving per day."
    )

    declination: Optional[float] = Field(
        None,
        title="Declination",
        description="The equatorial declination of the point."
    )
    declination_velocity: Optional[float] = Field(
        None,
        title="Declination Degrees Moved Per Day",
        description="The degrees from the equatorial that this point is moving per day."
    )

    sign: ZodiacSign = Field(
        ZodiacSign.aries,
        title="Zodiac Sign",
        description="The zodiac sign this point is located within."
    )
    modality: Modality = Field(
        Modality.cardinal,
        title="Zodiac Sign Modality",
        description="The modality of this point's zodiac sign."
    )
    element: Element = Field(
        Element.fire,
        title="Zodiac Sign Element",
        description="The element of this point's zodiac sign."
    )

    degrees_in_sign: int = Field(
        0,
        title="Degrees of current sign",
        description="The degrees, out of 30, that this point is located at within a sign."
    )
    minutes_in_degree: int = Field(
        0,
        title="Minutes of current degree",
        description="The minutes, out of 60, within a degree that this point is located at."
    )

    is_stationary: Optional[bool] = Field(
        None,
        title="Is Stationary",
        description="Whether this point is stationary on the ecliptic."
    )
    is_retrograde: Optional[bool] = Field(
        None,
        title="Is Retrograde",
        description="Whether this point is retrograde on the ecliptic."
    )

    houses_whole_sign: PointHousesSchema = Field(
        PointHousesSchema(),
        title="Whole Sign Houses",
        description="The whole sign house and ruled houses of this point."
    )
    houses_secondary: PointHousesSchema = Field(
        PointHousesSchema(),
        title="Secondary Houses",
        description="A secondary house system's house and ruled houses of this point."
    )

    rulers: PointRulersSchema = Field(
        PointRulersSchema(),
        title="Point Rulers",
        description="The rulers of the segment of the chart this point falls in."
    )

    condition: PointConditionSchema = Field(
        PointConditionSchema(),
        title="Condition",
        description="The state of bonification and maltreatment if this is a planet."
    )
