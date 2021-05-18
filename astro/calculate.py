from astro.chart.aspects import calculate_aspects
from astro.schema import Chart, ChartSettings
from astro.chart import create_all_points, create_summary, calculate_houses


def create_chart(settings: ChartSettings) -> Chart:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    start_points = create_all_points(settings.start)
    natal_points = [point for point in start_points.values()]

    results = Chart(
        start=settings.start,
        start_points=start_points,
        houses=calculate_houses(start_points),
        summary=create_summary(start_points),
        aspects=calculate_aspects(natal_points, natal_points, settings.orbs, True)
    )

    return results
