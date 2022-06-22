from datetime import datetime, timedelta
from typing import List
import re

from pydantic import Field

from astro.util import TransitGroupType
from .base import EventSchema, BaseSchema
from .aspect import AspectSchema
from .relationship import Point2PointSchema


class TransitEventSchema(EventSchema):
    """
    Represents an event that lasts some duration.
    """
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


class TransitSchema(AspectSchema, Point2PointSchema):
    """
    Represents information about the relationship between two points.
    """
    name: str = Field(
        ...,
        title="Name",
        description="The name of this transit."
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
        return f"{self.get_time()}: {self.name}"

    def get_full_name(self) -> str:
        """
        :return: The aspect and points for this transit, and whether it is precession corrected.
        """
        return f"{self.name} (PC)" if self.is_precession_corrected else self.name

    def get_time(self) -> str:
        """
        :return: The date, hours, and minutes when this transit goes exact.
        """
        timestamp = ':'.join(str(self.local_exact_date).split(':')[0:2])

        return re.sub(r"\d\d\d\d-", "", timestamp)


class TransitGroupSchema(BaseSchema):
    """
    Represents a group of transits with similar traits.
    """
    transits: List[TransitSchema] = Field(
        [],
        title="Transits",
        description="The transits in this group."
    )
    group_by: TransitGroupType = Field(
        TransitGroupType.all,
        title="Group By",
        description="How these transits are grouped."
    )
    group_value: str = Field(
        "",
        title="Grouped Group",
        description="The value these transits are grouped by, such as the planet."
    )
