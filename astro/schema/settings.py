from pydantic import Field

from .aspect import AspectOrbs
from .base import BaseSchema, DateTimeLocation


class ChartSettings(BaseSchema):
    """
    Defines the input parameters for running a calculation.

    - Default stationary speed is based on the equation described here:
      https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    - Default sun conjunction orbs uses ranges found here here:
      https://crystalbastrology.com/meaning-of-cazimi-in-astrology/
    """

    start: DateTimeLocation = Field(
        DateTimeLocation(),
        title="Start Time and Location",
        description="The base date, time, and location of calculations"
    )
    orbs: AspectOrbs = Field(
        AspectOrbs(),
        title="Aspect Orbs",
        description="The orbs to use for aspect calculations"
    )
    stationary_pct_of_avg_speed: float = Field(
        0.30,
        title="Stationary Speed Factor",
        description="The percent of the average speed of a planet that it must be under to be considered stationary"
    )
