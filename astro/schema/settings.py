from typing import List, Optional, Tuple

from pydantic import Field

from astro.util import Point, HouseSystem, AspectSortType, RulershipType
from .base import BaseSchema
from .event import EventSchema
from .point import PointSchema
from .transit import TransitSettingsSchema
from .enabled_points import EnabledPointsSchema, MidpointSchema


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
    transits: Optional[TransitSettingsSchema] = Field(
        None,
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
        AspectSortType.no_sort,
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

    calculate_condition: bool = Field(
        True,
        title="Do Calculate Condition",
        description="This flag enables the calculation of the condition of points."
    )
    calculate_divisions: bool = Field(
        True,
        title="Do Calculate Divisions",
        description="This flag enables the calculation of the condition of sign divisions."
    )
    calculate_relationships: bool = Field(
        True,
        title="Do Calculate Relationships",
        description="This flag enables the calculation of relationships between points."
    )
    calculate_relationship_phase: bool = Field(
        True,
        title="Do Calculate Relationship Phase",
        description="This flag enables the calculation the phase between points."
    )
    calculate_relationship_movement: bool = Field(
        True,
        title="Do Calculate Relationship Movement",
        description="This flag enables the calculation the application/separation between points."
    )
    remove_empty_relationships: bool = Field(
        True,
        title="Do Remove Empty Relationships",
        description="This flag will remove any point relationships with no ecliptic or declination aspects."
    )
