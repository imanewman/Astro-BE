from typing import List, Tuple

from astro.schema import PointSchema, RelationshipSchema, SettingsSchema
from .declination_aspect import calculate_declination_aspect
from .degree_aspect import calculate_degree_aspect
from .degree_types import calculate_degree_types
from .phase import calculate_aspect_phase
from .sign_aspect import calculate_sign_aspect
from astro.util import EventType


def calculate_relationships(
        from_items: Tuple[List[PointSchema], EventType],
        to_items: Tuple[List[PointSchema], EventType],
        is_natal: bool = False,
        settings: SettingsSchema = SettingsSchema()
) -> List[RelationshipSchema]:
    """
   Calculates the relationships between each set of 2 points.

   :param from_items: The points to calculate aspects from, and the event type.
   :param to_items: The points to calculate aspects to, and the event type.
   :param is_natal: If true, aspects will not be bi-directionally duplicated.
   :param settings: The settings to use for calculations.

   :return: All calculated relationships.
   """
    from_points, from_event_type = from_items
    to_points, to_event_type = to_items

    relationships = []

    for from_point in from_points:
        if is_natal:
            # For natal charts, skip the points that have been calculated already to avoid duplicates.
            to_points = to_points[1:]

        for to_point in to_points:
            relationship = RelationshipSchema(
                from_point=from_point.name,
                to_point=to_point.name
            )

            calculate_sign_aspect(relationship, from_point, to_point)
            calculate_degree_aspect(relationship, from_point, to_point, settings)
            calculate_aspect_phase(relationship, from_point, to_point)
            calculate_declination_aspect(relationship, from_point, to_point, settings)
            calculate_degree_types(
                relationship,
                (from_point, from_event_type),
                (to_point, to_event_type)
            )

            relationships.append(relationship)

    return relationships
