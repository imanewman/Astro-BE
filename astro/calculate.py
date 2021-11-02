from astro.schema import ChartSchema, SettingsSchema, ChartCollectionSchema, RelationshipCollectionSchema
from astro.chart import create_summary, calculate_houses, calculate_relationships, \
    calculate_condition, create_points_with_attributes, calculate_is_day_time


def create_chart(settings: SettingsSchema) -> ChartCollectionSchema:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """
    chart_count = len(settings.events)
    secondary_house_system = settings.secondary_house_system
    all_point_arrays = []
    all_charts = []
    all_relationships = []

    # Store each event's calculated points, conditions, and aspects.
    for event_index in range(chart_count):
        event_settings = settings.events[event_index]
        event = event_settings.event
        points = create_points_with_attributes(event_settings, settings)
        points_array = [point for point in points.values()]
        points_and_event_type = (points_array, event)

        relationships = calculate_relationships(
            points_and_event_type,
            points_and_event_type,
            True,
            settings
        )

        houses_whole_sign, houses_secondary = calculate_houses(points, event, secondary_house_system)
        is_day_time = calculate_is_day_time(points)

        calculate_condition(points, is_day_time)

        summary = create_summary(points, is_day_time)

        all_point_arrays.append(points_and_event_type)

        all_charts.append(ChartSchema(
            event=event,
            points=points,
            secondary_house_system=secondary_house_system,
            houses_whole_sign=houses_whole_sign,
            houses_secondary=houses_secondary,
            summary=summary,
        ))

        all_relationships.append(RelationshipCollectionSchema(
            from_chart_index=event_index,
            relationships=relationships
        ))

    # Store the aspects between all sets of distinct charts.
    for from_index in range(chart_count - 1):
        for to_index in range(from_index + 1, chart_count):
            relationships = calculate_relationships(
                all_point_arrays[from_index],
                all_point_arrays[to_index],
                False,
                settings
            )

            all_relationships.append(RelationshipCollectionSchema(
                from_chart_index=from_index,
                to_chart_index=to_index,
                relationships=relationships
            ))

    return ChartCollectionSchema(
        charts=all_charts,
        relationships=all_relationships
    )
