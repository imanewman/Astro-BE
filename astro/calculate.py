from astro.chart.condition import calculate_condition
from astro.chart.relationships import calculate_relationships
from astro.schema import Chart, ChartSettings
from astro.chart import create_all_points, create_summary, calculate_houses


def create_chart(settings: ChartSettings) -> Chart:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    start_points = create_all_points(settings.start, settings.stationary_pct_of_avg_speed)
    natal_points = [point for point in start_points.values()]
    houses = calculate_houses(start_points)
    summary = create_summary(start_points)
    relationships = calculate_relationships(natal_points, natal_points, True, settings.orbs)

    calculate_condition(start_points, summary.is_day_time)

    results = Chart(
        start=settings.start,
        start_points=start_points,
        houses=houses,
        summary=summary,
        relationships=relationships
    )

    return results
