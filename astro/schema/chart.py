from typing import Optional, List

from pydantic import Field

from astro.util import ZodiacSign, HouseSystem
from .types import PointMap
from .base import BaseSchema
from .event import EventSchema
from .relationship import RelationshipCollectionSchema
from .transit import TransitGroupSchema
from .house import HouseSchema


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
    points: PointMap = Field(
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
    transits: List[TransitGroupSchema] = Field(
        [],
        title="Transits",
        description="A list of transits from this chart to transiting points in this time range."
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

