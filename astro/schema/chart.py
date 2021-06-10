from typing import Optional, Dict, List

from pydantic import Field

from astro.util import ZodiacSign, Point
from .aspect import PointRelationship
from .house import HousePlacement
from .base import BaseSchema, EventSchema
from .point import PointInTime


class ChartSummary(BaseSchema):
    """
    Summarizes the most important details of a generated chart.
    """

    sun: ZodiacSign = Field(
        ...,
        title="Sun Sign",
        description="The current zodiac sign of the sun"
    )
    moon: ZodiacSign = Field(
        ...,
        title="Moon Sign",
        description="The current zodiac sign of the moon"
    )
    asc: ZodiacSign = Field(
        ...,
        title="Ascendant Sign",
        description="The current zodiac sign of the ascendant"
    )
    asc_ruler: Point = Field(
        ...,
        title="Ascendant Ruler",
        description="The ruling planet of the ascendant"
    )
    is_day_time: bool = Field(
        ...,
        title="Is Day Time",
        description="Whether the current time is during the day"
    )


class Chart(BaseSchema):
    """
    Defines the results returned after running a calculation.
    """

    start: EventSchema = Field(
        ...,
        title="Start Time and Location",
        description="The base date, time, and location of calculations"
    )
    summary: Optional[ChartSummary] = Field(
        None,
        title="Chart Summary",
        description="Summarizes the most important information in a chart"
    )
    start_points: Dict[Point, PointInTime] = Field(
        [],
        title="Planets and Points",
        description="A map of the base planets and points calculated"
    )
    houses: List[HousePlacement] = Field(
        [],
        title="Houses",
        description="Each house, its sign, and the points within it"
    )
    relationships: List[PointRelationship] = Field(
        [],
        title="Point Relationships",
        description="A list of relationships between every set of points in the chart"
    )
