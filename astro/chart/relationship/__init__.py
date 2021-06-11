from typing import List

from astro.schema import PointSchema, AspectOrbsSchema, RelationshipSchema
from .declination_aspect import calculate_declination_aspect
from .degree_aspect import calculate_degree_aspect
from .phase import calculate_aspect_phase
from .sign_aspect import calculate_sign_aspect


def calculate_relationships(
        from_points: List[PointSchema],
        to_points: List[PointSchema],
        is_natal: bool = False,
        orbs: AspectOrbsSchema = AspectOrbsSchema(),
) -> List[RelationshipSchema]:
    """
   Calculates the relationships between each set of 2 points.

   :param from_points: The points to calculate aspects from.
   :param to_points: The points to calculate aspects to.
   :param orbs: The orbs to use for calculations.
   :param is_natal: If true, aspects will not be bi-directionally duplicated.

   :return: All calculated relationships.
   """

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
            calculate_degree_aspect(relationship, from_point, to_point, orbs)
            calculate_aspect_phase(relationship, from_point, to_point)
            calculate_declination_aspect(relationship, from_point, to_point, orbs)

            relationships.append(relationship)

    return relationships
