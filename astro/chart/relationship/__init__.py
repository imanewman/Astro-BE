from typing import List, Tuple

from astro.schema import PointSchema, RelationshipSchema, SettingsSchema, EventSchema
from .declination_aspect import calculate_declination_aspect
from .ecliptic_aspect import calculate_ecliptic_aspect
from .aspect_movement import calculate_aspect_movement
from .phase import calculate_aspect_phase
from .sign_aspect import calculate_sign_aspect
from astro.util import AspectSortType


def calculate_relationships(
        from_items: Tuple[List[PointSchema], EventSchema],
        to_items: Tuple[List[PointSchema], EventSchema],
        is_natal: bool = False,
        settings: SettingsSchema = SettingsSchema()
) -> List[RelationshipSchema]:
    """
   Calculates the relationships between each set of 2 points.

   :param from_items: The points to calculate aspects from, and the event.
   :param to_items: The points to calculate aspects to, and the event.
   :param is_natal: If true, aspects will not be bi-directionally duplicated.
   :param settings: The settings to use for calculations.

   :return: All calculated relationships.
   """

    from_points, from_event = from_items
    to_points, to_event = to_items
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
            calculate_ecliptic_aspect(relationship, from_point, to_point, settings)
            calculate_aspect_phase(relationship, from_point, to_point)
            calculate_declination_aspect(relationship, from_point, to_point, settings)
            calculate_aspect_movement(
                relationship,
                (from_point, from_event),
                (to_point, to_event)
            )

            relationships.append(relationship)

    if settings.aspect_sort == AspectSortType.smallest_orb:
        # Sort ordered by the smallest orb
        def sort_smallest_rb(rel: RelationshipSchema) -> float:
            return abs(rel.ecliptic_aspect.orb or rel.declination_aspect.orb or 360)

        relationships.sort(key=sort_smallest_rb)

    return relationships
