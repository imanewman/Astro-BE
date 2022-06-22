from datetime import datetime
from typing import List

from pydantic import Field

from astro.util.enums import EventType
from .base import BaseSchema


class EventSchema(BaseSchema):
    """
    Defines a date and time at a geographic location.
    """
    name: str = Field(
        "Event",
        title="Event Name",
        description="The name of the person or event represented."
    )
    type: EventType = Field(
        EventType.event,
        title="Event Type",
        description="The general type of event this represents."
    )
    tags: List[str] = Field(
        [],
        title="Tags",
        description="Any tags this event is grouped by."
    )

    local_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Local Date",
        description="The local time for the location, defaulting to now."
    )
    utc_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="UTC Date",
        description="The UTC time for the location used for all calculations, defaulting to now."
    )
    timezone: str = Field(
        "Unknown",
        title="Timezone",
        description="The name of the timezone this event is in."
    )
    utc_offset: str = Field(
        "UTC-0.00",
        title="UTC Offset",
        description="The UTC offset time based on this event's timezone."
    )
    julian_day: float = Field(
        0,
        title="Julian Day",
        description="The standardized julian day for this date."
    )

    location: str = Field(
        "Unknown Location",
        title="Location",
        description="The name of the location of the event."
    )
    latitude: float = Field(
        0,
        title="Location Latitude",
        description="The latitude of the location."
    )
    longitude: float = Field(
        0,
        title="Location Longitude",
        description="The longitude of the location."
    )
