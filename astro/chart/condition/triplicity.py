from astro.schema import PointSchema
from astro.collection.zodiac_sign_traits import zodiac_sign_traits


def calculate_triplicity(point: PointSchema, is_day_time: bool):
    """
    Calculates the triplicity rulers for the given planet.

    - Swaps the first two triplicity rulers during the night.
    - Sets the point's condition to `in_triplicity` if this point is one of
      its element's triplicity rulers.

    :param point: The point to calculate the triplicity rulers for.
    :param is_day_time: Whether the point is found during the day.
    """

    traits = zodiac_sign_traits.signs[point.sign]

    point.condition.in_triplicity = point.name in traits.triplicity

    if is_day_time:
        point.rulers.triplicity = traits.triplicity
    else:
        point.rulers.triplicity = (traits.triplicity[1], traits.triplicity[0], traits.triplicity[2])
