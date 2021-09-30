from typing import Optional, Dict, List

from pydantic import Field

from astro.util import ZodiacSign, Point
from .aspect import RelationshipSchema, RelationshipCollectionSchema
from .house import HouseSchema
from .base import BaseSchema, EventSchema
from .point import PointSchema


class SummarySchema(BaseSchema):
    """
    Summarizes the most important details of a generated chart.
    """

    sun: Optional[ZodiacSign] = Field(
        None,
        title="Sun Sign",
        description="The current zodiac sign of the sun"
    )
    moon: Optional[ZodiacSign] = Field(
        None,
        title="Moon Sign",
        description="The current zodiac sign of the moon"
    )
    asc: Optional[ZodiacSign] = Field(
        None,
        title="Ascendant Sign",
        description="The current zodiac sign of the ascendant"
    )
    asc_ruler: Optional[Point] = Field(
        None,
        title="Ascendant Ruler",
        description="The ruling planet of the ascendant"
    )
    is_day_time: bool = Field(
        True,
        title="Is Day Time",
        description="Whether the current time is during the day"
    )


class ChartSchema(BaseSchema):
    """
    Defines a calculated chart's positions and condition.
    """

    event: EventSchema = Field(
        ...,
        title="Event Time and Location",
        description="The date, time, and location of calculations"
    )
    summary: Optional[SummarySchema] = Field(
        None,
        title="Chart Summary",
        description="Summarizes the most important information in a chart"
    )
    points: Dict[Point, PointSchema] = Field(
        [],
        title="Planets and Points",
        description="A map of the base planets and points calculated"
    )
    houses: List[HouseSchema] = Field(
        [],
        title="Houses",
        description="Each house, its sign, and the points within it"
    )


class ChartCollectionSchema(BaseSchema):
    """
    Defines a collection of multiple calculated charts, and the aspects between them.
    """
    charts: List[ChartSchema] = Field(
        [],
        title="Charts",
        description="A list of calculated chart points for given events"
    )
    relationships: List[RelationshipCollectionSchema] = Field(
        [],
        title="Relationships",
        description="A list of sets of relationships within and between each chart"
    )

