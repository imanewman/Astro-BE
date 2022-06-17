from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from pydantic import Field

from astro.util import Point, default_enabled_points, HouseSystem, AspectType, default_enabled_aspects, AspectSortType, \
    RulershipType
from . import PointSchema
from .aspect import AspectOrbsSchema
from .base import BaseSchema, EventSchema


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


class TransitSettingsSchema(BaseSchema):
    """
    Defines the transits to calculate the timing of for an event.
    """
    do_calculate_tropical: bool = Field(
        False,
        title="Do Calculate Transits",
        description="Determines whether the timing of transits should be calculated for an event."
    )
    do_calculate_precession_corrected: bool = Field(
        False,
        title="Do Calculate Transits (Precession Corrected)",
        description=
        "Determines whether the timing of transits, accounting for precession, should be calculated for an event."
    )
    start_date: datetime = Field(
        datetime.utcnow(),
        title="Transit Start Date",
        description="The starting date of the period to calculate transits within."
    )
    end_date: datetime = Field(
        datetime.utcnow() + timedelta(days=7),
        title="Transit End Date",
        description="The ending date of the period to calculate transits within."
    )


class EventSettingsSchema(BaseSchema):
    """
    Defines a single event to be calculated.
    """
    event: EventSchema = Field(
        EventSchema(),
        title="Start Time and Location",
        description="The base date, time, and location of calculations."
    )
    enabled: List[EnabledPointsSchema] = Field(
        [EnabledPointsSchema()],
        title="Enabled Points",
        description="Defines what points should be enabled for calculations. " +
                    "When calculating aspect between points in different enabled objects, " +
                    "orbs and aspect types will be taken from the latter of the two points."
    )
    transits: TransitSettingsSchema = Field(
        TransitSettingsSchema(),
        title="Transit Settings",
        description="The settings for transits to calculate for this event."
    )

    # progress_to: Optional[EventSchema] = Field(
    #     None,
    #     title="Progressed Start Time and Location",
    #     description="The progressed date, time, and location of calculations."
    # )
    # solar_arc_to: Optional[EventSchema] = Field(
    #     None,
    #     title="Solar Arc Start Time and Location",
    #     description="The solar arc date, time, and location of calculations."
    # )

    def get_all_enabled_points(self) -> List[Point]:
        """
        :return: Returns all enabled points.
        """
        points = []

        for enabled_points in self.enabled:
            points = [*points, *enabled_points.points]

        return points

    def get_all_enabled_midpoints(self) -> List[MidpointSchema]:
        """
        :return: Returns all enabled midpoints.
        """
        points = []

        for enabled_points in self.enabled:
            points = [*points, *enabled_points.midpoints]

        return points

    def get_enabled_for_point(
            self,
            point: PointSchema,
    ) -> Tuple[Optional[EnabledPointsSchema], Optional[int]]:
        """
        Returns the enabled points for this point.

        :param point: The point to search for.

        :return:
            [0] The enabled points.
            [1] The priority of the enabled points list,
                with higher numbers equal to higher priority.
        """
        idx = 0

        for enabled_points in self.enabled:
            if enabled_points.does_point_exist(point):
                return enabled_points, idx

            idx += 1

        return None, None


class SettingsSchema(BaseSchema):
    """
    Defines the input parameters for running a calculation.

    - Default stationary speed is based on the equation described here:
      https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/

    - Default sun conjunction orbs uses ranges found here:
      https://crystalbastrology.com/meaning-of-cazimi-in-astrology/
    """
    events: List[EventSettingsSchema] = Field(
        [],
        title="Events",
        description="The events to calculate positions and aspects for."
    )
    secondary_house_system: HouseSystem = Field(
        HouseSystem.porphyry,
        title="Secondary House System",
        description="The secondary house system to calculate, besides the default whole sign.",
    )
    aspect_sort: AspectSortType = Field(
        AspectSortType.closest_exact,
        title="Aspect Sort",
        description="The way to sort the aspects."
    )
    stationary_pct_of_avg_speed: float = Field(
        0.30,
        title="Stationary Speed Factor",
        description="The percent of the average speed of a planet that it must be under to be considered stationary."
    )
    rulership_system: List[RulershipType] = Field(
        [RulershipType.traditional, RulershipType.modern],
        title="Rulership System",
        description="The list of rulership systems to use in sign rulership calculations."
    )

    do_calculate_point_attributes: bool = Field(
        True,
        title="Do Calculate Point Attributes",
        description="This flag enables the calculation of all point attributes that arent directly from the ephemeris."
    )
    do_calculate_condition: bool = Field(
        True,
        title="Do Calculate Condition",
        description="This flag enables the calculation of the condition of points."
    )
    do_calculate_divisions: bool = Field(
        True,
        title="Do Calculate Divisions",
        description="This flag enables the calculation of the condition of sign divisions."
    )
    do_calculate_relationships: bool = Field(
        True,
        title="Do Calculate Relationships",
        description="This flag enables the calculation of relationships between points."
    )
    do_calculate_relationship_attributes: bool = Field(
        True,
        title="Do Calculate Relationship Attributes",
        description="This flag enables the calculation the phase and application/separation between points."
    )
