from typing import List, Optional

from pydantic import Field

from astro.util import Point, default_enabled_points, HouseSystem, AspectType, default_enabled_aspects
from .aspect import AspectOrbsSchema
from .base import BaseSchema, EventSchema


class EventSettingsSchema(BaseSchema):
    """
    Defines a single event to be calculated.
    """
    event: EventSchema = Field(
        EventSchema(),
        title="Start Time and Location",
        description="The base date, time, and location of calculations."
    )
    enabled_points: List[Point] = Field(
        default_enabled_points,
        title="Enabled Points",
        description="Defines what points should be enabled for calculations."
    )
    # TODO
    progress_to: Optional[EventSchema] = Field(
        None,
        title="Progressed Start Time and Location",
        description="The progressed date, time, and location of calculations."
    )
    # TODO
    solar_arc_to: Optional[EventSchema] = Field(
        None,
        title="Solar Arc Start Time and Location",
        description="The solar arc date, time, and location of calculations."
    )


class SettingsSchema(BaseSchema):
    """
    Defines the input parameters for running a calculation.

    - Default stationary speed is based on the equation described here:
      https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    - Default sun conjunction orbs uses ranges found here here:
      https://crystalbastrology.com/meaning-of-cazimi-in-astrology/
    """

    events: List[EventSettingsSchema] = Field(
        [],
        title="Events",
        description="The events to calculate positions and aspects for."
    )
    secondary_house_system: HouseSystem = Field(
        HouseSystem.porphyry,
        title="Secondary House System",
        description="The secondary house system to calculate, besides the default whole sign.",
    )
    orbs: AspectOrbsSchema = Field(
        AspectOrbsSchema(),
        title="Aspect Orbs",
        description="The orbs to use for aspect calculations."
    )
    enabled_aspects: List[AspectType] = Field(
        default_enabled_aspects,
        title="Enabled Aspects",
        description="Defines what aspects should be enabled for calculations."
    )
    stationary_pct_of_avg_speed: float = Field(
        0.30,
        title="Stationary Speed Factor",
        description="The percent of the average speed of a planet that it must be under to be considered stationary."
    )

