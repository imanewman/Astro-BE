from typing import List

from pydantic import Field

from astro.util import Point, default_enabled_points, AspectType, default_enabled_aspects
from .base import BaseSchema
from .point import PointSchema
from .aspect import AspectOrbsSchema


class MidpointSchema(BaseSchema):
    """
    Defines a midpoint to calculate for a specific event.
    """
    def __str__(self):
        return f"{self.from_point}-{self.to_point} Midpoint"

    from_point: Point = Field(
        None,
        title="From Point",
        description="Defines the point to calculate a midpoint from."
    )
    to_point: Point = Field(
        None,
        title="To Point",
        description="Defines the point to calculate a midpoint to."
    )


class EnabledPointsSchema(BaseSchema):
    """
    Defines what points to calculate and how to calculate relationships between them.
    """
    points: List[Point] = Field(
        default_enabled_points,
        title="Enabled Points",
        description="Defines what points should be enabled for calculations."
    )
    midpoints: List[MidpointSchema] = Field(
        [],
        title="Enabled Midpoints",
        description="Defines what midpoints should be enabled for calculations."
    )

    orbs: AspectOrbsSchema = Field(
        AspectOrbsSchema(),
        title="Aspect Orbs",
        description="The orbs to use for aspect calculations."
    )
    aspects: List[AspectType] = Field(
        default_enabled_aspects,
        title="Enabled Aspects",
        description="Defines what aspects should be enabled for calculations."
    )

    def does_point_exist(
            self,
            point: PointSchema,
    ) -> bool:
        """
        Returns whether the given point or midpoint is in these settings.

        :param point: The point to search for.

        :return: Whether the point or midpoint exists.
        """
        point_names = point.points

        if len(point_names) == 2:
            for midpoint in self.midpoints:
                if midpoint.from_point == point_names[0] and midpoint.to_point == point_names[1]:
                    return True

        return point.name in self.points
