from astro.schema import ChartSchema, SettingsSchema, ChartCollectionSchema, RelationshipCollectionSchema
from astro.chart import create_summary, calculate_houses, calculate_relationships, \
    calculate_condition, create_points_with_attributes, calculate_is_day_time, calculate_transits


def create_chart(settings: SettingsSchema) -> ChartCollectionSchema:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings.

    :return: Calculated points and aspects.
    """
    chart_count = len(settings.events)
    all_points_and_events = []
    all_charts = []
    all_relationships = []

    # Store each event's calculated points, conditions, and aspects.
    for event_index in range(chart_count):
        event_settings = settings.events[event_index]
        event = event_settings.event

        points = create_points_with_attributes(event_settings, settings)
        points_array = [point for point in points.values()]
        points_and_event = (points_array, event_settings)

        is_day_time = calculate_is_day_time(points)
        summary = create_summary(points, is_day_time)
        houses_whole_sign, houses_secondary = calculate_houses(points, event, settings)
        calculate_condition(points, is_day_time, settings)
        calculate_transits(event_settings, points_array)

        relationships = calculate_relationships(
            points_and_event,
            points_and_event,
            True,
            settings
        )

        all_points_and_events.append(points_and_event)

        all_charts.append(ChartSchema(
            event=event,
            points=points,
            secondary_house_system=settings.secondary_house_system,
            houses_whole_sign=houses_whole_sign,
            houses_secondary=houses_secondary,
            summary=summary,
        ))

        all_relationships.append(RelationshipCollectionSchema(
            from_chart_index=event_index,
            from_chart_type=event.type,
            to_chart_index=event_index,
            to_chart_type=event.type,
            name=f"{event.name} & {event.name}",
            relationships=relationships
        ))

    # Store the aspects between all sets of distinct charts.
    for from_index in range(chart_count - 1):
        for to_index in range(from_index + 1, chart_count):
            from_event = all_points_and_events[from_index][1].event
            to_event = all_points_and_events[to_index][1].event

            relationships = calculate_relationships(
                all_points_and_events[from_index],
                all_points_and_events[to_index],
                False,
                settings
            )

            all_relationships.append(RelationshipCollectionSchema(
                from_chart_index=from_index,
                from_chart_type=from_event.type,
                to_chart_index=to_index,
                to_chart_type=to_event.type,
                name=f"{from_event.name} & {to_event.name}",
                relationships=relationships
            ))

    return ChartCollectionSchema(
        charts=all_charts,
        relationships=all_relationships
    )
