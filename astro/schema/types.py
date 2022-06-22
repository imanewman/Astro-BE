from typing import Tuple, Dict

from astro.schema import EventSettingsSchema, PointSchema, RelationshipSchema
from astro.util import Point

PointMap = Dict[Point, PointSchema]
"""
A map from point names to calculated points.
"""

RelationshipMap = Dict[str, RelationshipSchema]
"""
A map from relationship names to calculated relationships.
"""

TransitIncrement = Tuple[
    EventSettingsSchema,
    PointMap,
    RelationshipMap
]
"""
Represents a calculated set of an event, its points, and the relationships with 
"""