from datetime import datetime
from typing import List

from humps import camelize
from pydantic import BaseModel, Field

from astro.util.enums import EventType


class BaseSchema(BaseModel):
    """
    A base schema that all models inherit configuration from.
    """

    class Config:
        # CamelCase to snake_case translation automatically for every field
        alias_generator = camelize
        # Create the Pydantic models normally from python with snake_case
        allow_population_by_field_name = True
        # Strip extra whitespace around strings
        anystr_strip_whitespace = True
        # Try to access attributes by dot notation
        orm_mode = True
        # Make private attributes that won’t show up in the docs
        underscore_attrs_are_private = True
        # Gives you strings instead of the Enum class if you use enums anywhere
        use_enum_values = True


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
        title="Date",
        description="The local time for the location, defaulting to now."
    )
    utc_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Date",
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
