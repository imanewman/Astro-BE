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

    if event_settings.transits.group_by == TransitGroupType.by_day:
        for transit in transits:
            day = transit.get_time().split(" ")[0]

            if day not in groups:
                groups[day] = TransitGroupSchema(
                    group_by=TransitGroupType.by_day,
                    group_value=day
                )

            groups[day].transits.append(transit)

    elif event_settings.transits.group_by == TransitGroupType.by_natal_point:
        for transit in transits:
            point = transit.to_point

            if point not in groups:
                groups[point] = TransitGroupSchema(
                    group_by=TransitGroupType.by_natal_point,
                    group_value=point
                )

            groups[point].transits.append(transit)

        return list(groups.values())

    elif event_settings.transits.group_by == TransitGroupType.by_transit_point:
        for transit in transits:
            point = transit.from_point

            if point not in groups:
                groups[point] = TransitGroupSchema(
                    group_by=TransitGroupType.by_transit_point,
                    group_value=point
                )

            groups[point].transits.append(transit)

    elif event_settings.transits.group_by == TransitGroupType.by_relationship:
        for transit in transits:
            if transit.name not in groups:
                groups[transit.name] = TransitGroupSchema(
                    group_by=TransitGroupType.by_relationship,
                    group_value=transit.name
                )

            groups[transit.name].transits.append(transit)

        return list(groups.values())

    else:
        groups["all"] = TransitGroupSchema(transits=transits)

    return list(groups.values())
