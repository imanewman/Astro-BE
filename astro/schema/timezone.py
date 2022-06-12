from datetime import datetime
from pydantic import Field

from .base import BaseSchema


class TimezoneQuerySchema(BaseSchema):
    """
    Defines a details needed to query for a timezone.
    """
    location_name: str = Field(
        ...,
        title="Location Name",
        description="The name of the location for the timezone."
    )
    local_date: datetime = Field(
        ...,
        title="Local Date",
        description="The local time and date to convert into UTC."
    )


class TimezoneSchema(TimezoneQuerySchema):
    """
    Defines a timezone for a specific location.
    """
    time_zone_id: str = Field(
        "",
        title="Timezone ID",
        description="The standard ID for this timezone."
    )
    time_zone_name: str = Field(
        "",
        title="Timezone Name",
        description="The name for this timezone."
    )
    dst_offset: int = Field(
        0,
        title="DST Offset",
        description="The daylight savings time offset for this timezone."
    )
    raw_offset: int = Field(
        0,
        title="UTC Offset",
        description="The UTC offset in milliseconds for this time zone."
    )
    latitude: float = Field(
        0,
        title="Latitude",
        description="The latitude of the location."
    )
    longitude: float = Field(
        0,
        title="Longitude",
        description="The longitude of the location."
    )
    utc_date: datetime = Field(
        datetime.now(),
        title="UTC Date",
        description="The UTC time for the local date within this timezone."
    )
