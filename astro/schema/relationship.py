from typing import Optional, List, Union

from pydantic import Field

from astro.util import AspectType, Point, PhaseType, EventType
from .base import BaseSchema
from .aspect import AspectSchema


class Point2PointSchema(BaseSchema):
    """
    Represents 2 points between one or two events.
    """
    from_point: Union[Point, str] = Field(
        ...,
        title="From Point",
        description="The point this aspect is from."
    )
    from_type: Optional[EventType] = Field(
        None,
        title="From Type",
        description="The type of event this aspect is from."
    )

    to_point: Union[Point, str] = Field(
        ...,
        title="To Point",
        description="The point this aspect is to."
    )
    to_type: Optional[EventType] = Field(
        None,
        title="To Type",
        description="The type of event this aspect is to."
    )

    def get_from(self) -> str:
        """
        :return: The point and event type this aspect is from.
        """
        return f'{self.from_type} {self.from_point}'

    def get_to(self) -> str:
        """
        :return: The point and event type this aspect is to.
        """
        return f'{self.to_type} {self.to_point}'


class RelationshipSchema(Point2PointSchema):
    """
    Represents information about the relationship between two points.
    """
    arc_ordered: Optional[float] = Field(
        None,
        title="Ecliptic Degrees Between",
        description="The degrees between the two points relative to their longitude along the ecliptic. "
                    "This value will always be the arc from the first to the second point."
    )
    arc_minimal: Optional[float] = Field(
        None,
        title="Ecliptic Degrees Between",
        description="The arc between the two points relative to their longitude along the ecliptic. "
                    "This value will always be the smaller arc between the two points."
    )
    declination_arc: Optional[float] = Field(
        None,
        title="Declination Degrees Arc",
        description="The degrees between the two points relative to their declination from the equator."
    )

    phase: Optional[PhaseType] = Field(
        None,
        title="Phase",
        description="The phase of separation between these two points."
    )
    phase_base_point: Optional[Point] = Field(
        None,
        title="Phase Base Point",
        description="The point being used as the base for the phase between points."
    )

    precession_correction: float = Field(
        0,
        title="Precession Correction",
        description="The precession correction in degrees from the first to the second event."
    )

    sign_aspect: Optional[AspectType] = Field(
        None,
        title="Sign Based Aspect",
        description="The type of aspect by sign between the points."
    )
    ecliptic_aspect: AspectSchema = Field(
        AspectSchema(),
        title="Ecliptic Aspect",
        description="The aspect between the two points based on ecliptic longitude."
    )
    precession_corrected_aspect: AspectSchema = Field(
        AspectSchema(is_precession_corrected=True),
        title="Precession Corrected Ecliptic Aspect",
        description="The aspect between the two points based on ecliptic longitude, corrected for precession."
    )
    declination_aspect: AspectSchema = Field(
        AspectSchema(),
        title="Declination Aspect",
        description="The aspect between the two points based on declination."
    )

    def __str__(self):
        return f"{self.get_name}: {self.get_aspects()}"

    def get_name(self) -> str:
        return f'{self.from_point} To {self.to_point}'

    def get_aspects(self) -> List[AspectSchema]:
        """
        Returns all aspects in this relationship.

        :return: A list of aspects.
        """
        return [
            self.ecliptic_aspect,
            self.precession_corrected_aspect,
            self.declination_aspect
        ]


class RelationshipCollectionSchema(BaseSchema):
    """
    Represents the relationships between all points.
    """
    from_chart_index: int = Field(
        0,
        title="From Chart Index",
        description="The index of the chart that these aspects are calculated going from."
    )
    from_chart_type: str = Field(
        "",
        title="From Chart Type",
        description="The type of the chart that these aspects are calculated going from."
    )
    to_chart_index: int = Field(
        0,
        title="To Chart Index",
        description="The index of the chart that these aspects are calculated going to."
    )
    to_chart_type: str = Field(
        "",
        title="To Chart Type",
        description="The type of the chart that these aspects are calculated going to."
    )
    name: str = Field(
        "",
        title="Relationships Name",
        description="The name of these relationships."
    )
    relationships: List[RelationshipSchema] = Field(
        [],
        title="Relationships",
        description="A list of relationships between every set of points in the first to the second chart."
    )
