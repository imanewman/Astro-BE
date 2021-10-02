from astro import calculate_relationships
from astro.util import AspectType, EventType
from test.utils import create_test_points


def test_calculate_aspects():
    """
    Tests calculating all aspects for a set of planets.
    """

    points = create_test_points(
        {"degrees_from_aries": 0, "declination": 11, "house": 1},
        {"degrees_from_aries": 5, "declination": -11, "house": 1},
    )

    points_and_event_type = (points, EventType.event)
    aspects = calculate_relationships(points_and_event_type, points_and_event_type, True)

    assert len(aspects) is 1
    assert aspects[0].degree_aspect == AspectType.conjunction
    assert aspects[0].sign_aspect == AspectType.conjunction
    assert aspects[0].declination_aspect == AspectType.contraparallel


