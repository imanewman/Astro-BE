from pydantic import Field

from .aspect import AspectOrbs
from .base import BaseSchema, DateTimeLocation


class ChartSettings(BaseSchema):
    """
    Defines the input parameters for running a calculation.
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
