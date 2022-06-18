from datetime import datetime, timedelta
from typing import Union
import re

from pydantic import Field

from astro.util import Point
from .base import EventSchema
from .aspect import AspectSchema


class TransitEventSchema(EventSchema):
    local_end_date: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=7),
        title="Local End Date",
        description="The local time for the end of the date range, defaulting to 7 days from now."
    )
    utc_end_date: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=7),
        title="UTC End Date",
        description="The UTC time for the end of the date range, defaulting to 7 days from now."
    )


class TransitSchema(AspectSchema):
    """
    Represents information about the relationship between two points.
    """
    from_point: Union[Point, str] = Field(
        ...,
        title="From Point",
        description="The point this aspect is from."
    )
    to_point: Union[Point, str] = Field(
        ...,
        title="To Point",
        description="The point this aspect is to."
    )
    local_exact_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Local Exact Date",
        description="The local time when this aspect goes exact."
    )
    utc_exact_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="UTC Exact Date",
        description="The UTC time when this aspect goes exact."
    )

    def __str__(self):
        return f"{self.get_time()}: {self.get_name()}"

    def get_name(self) -> str:
        pc = " PC" if self.is_precession_corrected else ""

        return f"{self.from_point} {self.type}{pc} {self.to_point}"

    def get_time(self) -> str:
        timestamp = ':'.join(str(self.local_exact_date).split(':')[0:2])

        return re.sub(r"\d\d\d\d-", "", timestamp)
