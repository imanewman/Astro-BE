from datetime import datetime, timedelta
from typing import List, Optional
import re

from pydantic import Field

from astro.util import TransitGroupType, TransitType, ZodiacSign, TransitCalculationType
from .base import BaseSchema
from .event import EventSchema
from .enabled_points import EnabledPointsSchema
from .aspect import AspectSchema
from .relationship import Point2PointSchema


class TransitEventSchema(EventSchema):
    """
    Represents an event that lasts some duration.
    """
    local_end_date: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=7),
        title="Local End Date",
        description="The local time for the end of the date range, defaulting to 7 days from now."
    )
    utc_end_date: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=7),
        title="UTC End Date",
        description="The UTC time for the end of the date range, defaulting to 7 days from now."
    )


class TransitSettingsSchema(BaseSchema):
    """
    Defines the transits to calculate the timing of for an event.
    """
    type: TransitCalculationType = Field(
        TransitCalculationType.transit_to_chart,
        title="Transit Type",
        description="Whether to calculate aspects between transiting bodies, or to a static event."
    )
    event: TransitEventSchema = Field(
        TransitEventSchema(),
        title="Transit Event",
        description="The time range to calculate transits within."
    )
    enabled: List[EnabledPointsSchema] = Field(
        [EnabledPointsSchema()],
        title="Enabled Points",
        description="Defines what points should be enabled for transits. " +
                    "When calculating aspect between points in different enabled objects, " +
                    "orbs and aspect types will be taken from the latter of the two points."
    )

    hours_per_poll: float = Field(
        1,
        title="Hours Per Poll",
        description="How many times to poll before approximating transits." +
                    "Defaults to 1 hour. 0.5 will poll every 30 minutes. 2 will poll every 2 hours."
    )
    group_by: TransitGroupType = Field(
        TransitGroupType.all,
        title="Group By",
        description="How to group these transits."
    )

    do_calculate_ecliptic: bool = Field(
        True,
        title="Do Calculate Transits",
        description="Determines whether the timing of transits should be calculated for an event."
    )
    do_calculate_declination: bool = Field(
        False,
        title="Do Calculate Transits (Precession Corrected)",
        description=
        "Determines whether the timing of transits, accounting for precession, should be calculated for an event."
    )
    do_calculate_precession_corrected: bool = Field(
        False,
        title="Do Calculate Transits (Precession Corrected)",
        description=
        "Determines whether the timing of transits, accounting for precession, should be calculated for an event."
    )
    do_calculate_ingress: bool = Field(
        False,
        title="Do Calculate Ingresses",
        description="Determines whether to calculate ingresses. Only works for mundane transits."
    )
    do_calculate_station: bool = Field(
        False,
        title="Do Calculate Stations",
        description="Determines whether to calculate stations. Only works for mundane transits."
    )

    def is_one_chart(self) -> bool:
        """
        :return: Whether these transit settings are for calculating mundane transits.
        """
        return self.type == TransitCalculationType.transit_to_transit

    def do_calculate_aspects(self) -> bool:
        """
        :return: Whether to calculate aspects.
        """
        return self.do_calculate_ecliptic or self.do_calculate_declination or self.do_calculate_precession_corrected

    def do_calculate_points(self) -> bool:
        """
        :return: Whether to calculate points.
        """
        return self.do_calculate_ingress or self.do_calculate_station

    def do_calculate(self) -> bool:
        """
        :return: Whether to calculate transits at all.
        """
        time_is_valid = self.event.utc_date < self.event.utc_end_date

        return time_is_valid and (self.do_calculate_aspects() or self.do_calculate_points())


class TransitSchema(AspectSchema, Point2PointSchema):
    """
    Represents information about the relationship between two points.
    """
    name: str = Field(
        ...,
        title="Name",
        description="The name of this transit."
    )
    transit_type: TransitType = Field(
        TransitType.aspect,
        title="Transit",
        description="The type of this transit."
    )
    sign: Optional[ZodiacSign] = Field(
        None,
        title="Ingress Sign",
        description="For ingresses, the sign of the ingress."
    )

    local_exact_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="Local Exact Date",
        description="The local time when this aspect goes exact."
    )
    utc_exact_date: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        title="UTC Exact Date",
        description="The UTC time when this aspect goes exact."
    )

    def __str__(self):
        return f"{self.get_time()}: {self.name}"

    def get_full_name(self) -> str:
        """
        :return: The aspect and points for this transit, and whether it is precession corrected.
        """
        return f"{self.name} (PC)" if self.is_precession_corrected else self.name

    def get_time(self) -> str:
        """
        :return: The date, hours, and minutes when this transit goes exact.
        """
        timestamp = ':'.join(str(self.local_exact_date).split(':')[0:2])

        return re.sub(r"\d\d\d\d-", "", timestamp)


class TransitGroupSchema(BaseSchema):
    """
    Represents a group of transits with similar traits.
    """
    transits: List[TransitSchema] = Field(
        [],
        title="Transits",
        description="The transits in this group."
    )
    group_by: TransitGroupType = Field(
        TransitGroupType.all,
        title="Group By",
        description="How these transits are grouped."
    )
    group_value: str = Field(
        "",
        title="Grouped Group",
        description="The value these transits are grouped by, such as the planet."
    )
