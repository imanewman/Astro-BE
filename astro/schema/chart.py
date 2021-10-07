from typing import Optional, Dict, List

from pydantic import Field

from astro.util import ZodiacSign, Point, HouseSystem
from .aspect import RelationshipCollectionSchema
from .house import HouseSchema
from .base import BaseSchema, EventSchema
from .point import PointSchema


class SummarySchema(BaseSchema):
    """
    Summarizes the most important details of a generated chart.
    """

    is_day_time: bool = Field(
        True,
        title="Is Day Time",
        description="Whether the current time is during the day."
    )
    sun: Optional[ZodiacSign] = Field(
        None,
        title="Sun Sign",
        description="The current zodiac sign of the sun."
    )
    moon: Optional[ZodiacSign] = Field(
        None,
        title="Moon Sign",
        description="The current zodiac sign of the moon."
    )
    asc: Optional[ZodiacSign] = Field(
        None,
        title="Ascendant Sign",
        description="The current zodiac sign of the ascendant."
    )
    asc_ruler_sign: Optional[Point] = Field(
        None,
        title="Ascendant Sign Ruler",
        description="The ruling planet of the ascendant's sign."
    )
    asc_ruler_decan: Optional[Point] = Field(
        None,
        title="Ascendant Decan Ruler",
        description="The ruling planet of the ascendant's decan."
    )
    asc_ruler_bound: Optional[Point] = Field(
        None,
        title="Ascendant Bound Ruler",
        description="The ruling planet of the ascendant's bound."
    )


class ChartSchema(BaseSchema):
    """
    Defines a calculated chart's positions and condition.
    """

    event: EventSchema = Field(
        ...,
        title="Event Time and Location",
        description="The date, time, and location of calculations."
    )
    summary: Optional[SummarySchema] = Field(
        None,
        title="Chart Summary",
        description="Summarizes the most important information in a chart."
    )
    points: Dict[Point, PointSchema] = Field(
        [],
        title="Planets and Points",
        description="A map of the base planets and points calculated."
    )
    secondary_house_system: HouseSystem = Field(
        HouseSystem.whole_sign,
        title="Secondary House System",
        description="The secondary house system calculated.",
    )
    houses_whole_sign: List[HouseSchema] = Field(
        [],
        title="Whole Sign Houses",
        description="Each whole sign house, its sign, and the points within it."
    )
    houses_secondary: List[HouseSchema] = Field(
        [],
        title="Secondary Houses",
        description="Each secondary house, its sign, and the points within it."
    )


class ChartCollectionSchema(BaseSchema):
    """
    Defines a collection of multiple calculated charts, and the aspects between them.
    """

    charts: List[ChartSchema] = Field(
        [],
        title="Charts",
        description="A list of calculated chart points for given events."
    )
    relationships: List[RelationshipCollectionSchema] = Field(
        [],
        title="Relationships",
        description="A list of sets of relationships within and between each chart."
    )

