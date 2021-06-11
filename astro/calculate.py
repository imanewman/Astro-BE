from astro.schema import ChartSchema, SettingsSchema
from astro.chart import create_summary, calculate_houses, calculate_relationships, \
    calculate_condition, create_points_with_attributes


def create_chart(settings: SettingsSchema) -> ChartSchema:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    start_points = create_points_with_attributes(settings.start, settings)
    natal_points = [point for point in start_points.values()]
    houses = calculate_houses(start_points)
    summary = create_summary(start_points)
    relationships = calculate_relationships(natal_points, natal_points, True, settings.orbs)

    calculate_condition(start_points, summary.is_day_time)

    results = ChartSchema(
        start=settings.start,
        start_points=start_points,
        houses=houses,
        summary=summary,
        relationships=relationships
    )

    return results
