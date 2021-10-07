from typing import List, Optional

from pydantic import Field

from .base import BaseSchema
from ..util import ZodiacSign, Point


class HouseSchema(BaseSchema):
    """
    Defines the input parameters for running a calculation.
    """

    number: int = Field(
        ...,
        title="House Number",
        description="The number of this house",
        ge=1,
        le=12
    )
    sign: ZodiacSign = Field(
        ...,
        title="Zodiac Sign",
        description="The zodiac sign on the cusp of this house"
    )
    points: List[Point] = Field(
        [],
        title="Points",
        description="Any planets and points within this house"
    )
    from_longitude: Optional[float] = Field(
        None,
        title="Starting Longitude",
        description="The longitude of the beginning of the house."
    )
    to_longitude: Optional[float] = Field(
        None,
        title="Ending Longitude",
        description="The longitude of the end of the house."
    )
