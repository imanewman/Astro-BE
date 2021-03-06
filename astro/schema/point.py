from typing import Optional, List, Union

from pydantic import Field

from astro.util import ZodiacSign, Point, SectPlacement, Modality, Element, HouseSystem, SunCondition
from .base import BaseSchema


class PointConditionSchema(BaseSchema):
    """
    Defines the condition of a planet.
    For points that aren't planets, all values are false.
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


class DivisionsSchema(BaseSchema):
    """
    Defines the segments of the chart that this point falls in.
    """
    sign_ruler: Optional[Point] = Field(
        None,
        title="Sign Ruler",
        description="The traditional planet that rules this sign.",
    )
    decan_ruler: Optional[Point] = Field(
        None,
        title="Decan Ruler",
        description="The traditional planet that rules this decan.",
    )
    bound_ruler: Optional[Point] = Field(
        None,
        title="Bound Ruler",
        description="The traditional planet that rules this bound.",
    )
    triplicity_ruler: List[Point] = Field(
        [],
        title="Triplicity Ruler",
        description="The traditional planets that rule this element in the order of importance.",
    )
    twelfth_part_sign: Optional[ZodiacSign] = Field(
        None,
        title="12th Part Sign",
        description="The 12th part sign that this point is in."
    )
    degree_sign: Optional[ZodiacSign] = Field(
        None,
        title="Degree Sign",
        description="The sign corresponding to the degree of this point."
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


class MinimalPointSchema(BaseSchema):
    """
    Minimally defines any planetary body's position relative to Earth.
    """
    name: Union[Point, str] = Field(
        ...,
        title="Planet or Point",
        description="The name of the planet or point."
    )
    points: List[Point] = Field(
        ...,
        title="Points",
        description="The points composited to create this point."
    )

    sign: Optional[ZodiacSign] = Field(
        None,
        title="Zodiac Sign",
        description="The zodiac sign this point is located within."
    )
    modality: Optional[Modality] = Field(
        None,
        title="Zodiac Sign Modality",
        description="The modality of this point's zodiac sign."
    )
    element: Optional[Element] = Field(
        None,
        title="Zodiac Sign Element",
        description="The element of this point's zodiac sign."
    )

    def is_midpoint(self):
        """
        :return: Returns true if this point represents a midpoint.
        """
        return len(self.points) == 2


class PointSchema(MinimalPointSchema):
    """
    Defines any planetary body's position relative to Earth.
    """
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

    degrees_in_sign: Optional[int] = Field(
        None,
        title="Degrees of current sign",
        description="The degrees, out of 30, that this point is located at within a sign."
    )
    minutes_in_degree: Optional[int] = Field(
        None,
        title="Minutes of current degree",
        description="The minutes, out of 60, within a degree that this point is located at."
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

    divisions: DivisionsSchema = Field(
        DivisionsSchema(),
        title="Point Divisions",
        description="The segments of the chart that this point falls in."
    )
    condition: PointConditionSchema = Field(
        PointConditionSchema(),
        title="Condition",
        description="The condition of this is a planet."
    )
