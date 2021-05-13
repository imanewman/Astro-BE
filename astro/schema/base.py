from datetime import datetime

from humps import camelize
from pydantic import BaseModel, Field


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


class DateTimeLocation(BaseSchema):
    """
    Defines a time and a day at a geographic location.
    """

    date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Date",
        description="The UTC date to use, defaulting to now"
    )
    latitude: float = Field(
        36.0544,
        title="Location Latitude",
        description="The latitude of the location, defaulting to Grand Canyon, AZ"
    )
    longitude: float = Field(
        -112.1401,
        title="Location Longitude",
        description="The longitude of the location, defaulting to Grand Canyon, AZ"
    )