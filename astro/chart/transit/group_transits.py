from typing import List

from astro.schema import EventSettingsSchema, TransitSchema, TransitGroupSchema
from astro.util import TransitGroupType


def group_transits(
        event_settings: EventSettingsSchema,
        transits: List[TransitSchema]
) -> List[TransitGroupSchema]:
    """
    Groups transits by shared fields.

    :param event_settings: The current time, location, enabled points, and transit settings.
    :param transits: The transits to group.

    :return: The grouped transits.
    """
    groups = {}
    groupings = event_settings.transits.group_by

    for transit in transits:
        group_values = []

        if TransitGroupType.by_day in groupings:
            group_values.append(transit.get_time().split(" ")[0])
        if TransitGroupType.by_natal_point in groupings:
            group_values.append(transit.to_point)
        if TransitGroupType.by_transit_point in groupings:
            group_values.append(transit.from_point)
        if TransitGroupType.by_relationship in groupings:
            group_values.append(transit.name)
        if TransitGroupType.all in groupings:
            group_values.append("all")

        group = ", ".join(group_values)

        if group not in groups:
            groups[group] = TransitGroupSchema(
                group_by=groupings,
                group_value=group
            )

        groups[group].transits.append(transit)

    return list(groups.values())
