from typing import Optional, List, Union

from pydantic import Field

from astro.util import AspectType, Point, PhaseType, applying_aspects
from .base import BaseSchema
from .aspect import AspectSchema


class RelationshipSchema(BaseSchema):
    """
    Represents information about the relationship between two points.
    """
    from_point: Union[Point, str] = Field(
        ...,
        title="From Point",
        description="The point this aspect is from."
    )
    to_point: Union[Point, str] = Field(
        ...,
        title="To Point",
        description="The point this aspect is to."
    )

    sign_aspect: Optional[AspectType] = Field(
        None,
        title="Sign Based Aspect",
        description="The type of aspect by sign between the points."
    )

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
        return f'{self.get_aspect_name()}: {", ".join(self.get_applying_aspect_descriptions())}'

    def get_aspect_name(self) -> str:
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

    def get_applying_aspects(self) -> List[AspectSchema]:
        """
        Returns all aspects that have an upcoming approximate exact date.

        :return: A list of aspects.
        """
        return list(filter(
            lambda aspect: aspect.days_until_exact and aspect.movement in applying_aspects,
            self.get_aspects()
        ))

    def has_applying_aspects(self) -> bool:
        """
        Returns whether any aspect has an upcoming date.

        :return: Whether any aspect is closely applying.
        """
        return len(self.get_applying_aspects()) > 0

    def get_applying_aspect_descriptions(self) -> List[str]:
        aspects_strings = []
        aspect_types = []

        for aspect in self.get_applying_aspects():
            try:
                existing_type_index = aspect_types.index(aspect.type)

                aspects_strings[existing_type_index] = \
                    aspects_strings[existing_type_index].replace("]", f"]{aspect.get_date_stamp()}")
            except ValueError:
                aspects_strings.append(f'{aspect} From {self.get_aspect_name()}')

            aspect_types.append(aspect.type)

        return aspects_strings


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
