from humps import camelize
from pydantic import BaseModel


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
