from astro.schema import Chart, ChartSettings
from astro.chart import create_all_points, create_summary, calculate_houses


def create_chart(settings: ChartSettings) -> Chart:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    start_points = create_all_points(settings.start)

    results = Chart(
        start=settings.dict(),
        start_points=start_points,
        houses=calculate_houses(start_points),
        summary=create_summary(start_points),
    )

    return results
