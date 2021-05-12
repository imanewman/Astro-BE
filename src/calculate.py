from src.models import CalculationSettings, CalculationResults
from src.points import create_all_points
from src.summary import create_summary


def create_results(settings: CalculationSettings) -> CalculationResults:
    """
    Calculates the default settings for the given time.

    :param settings: The current calculation settings, including the time and location.

    :return: Calculated points and aspects.
    """

    start_points = create_all_points(settings.start)

    results = CalculationResults(
        start=settings.dict(),
        start_points=start_points,
        summary=create_summary(start_points)

    )

    return results
