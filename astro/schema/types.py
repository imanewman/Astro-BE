from typing import Tuple, Dict

from astro.schema import EventSettingsSchema, PointSchema, RelationshipSchema
from astro.util import Point

PointMap = Dict[Point, PointSchema]
RelationshipMap = Dict[str, RelationshipSchema]

Increment = Tuple[
    EventSettingsSchema,
    PointMap,
    RelationshipMap
]
"""
Represents a calculated set of an event, its points, and the relationships with 
"""