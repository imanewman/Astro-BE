from astro import calculate_relationships
from astro.util import AspectType, EventType
from astro.util.tim import tim_natal
from test.utils import create_test_points


def test_calculate_aspects():
    """
    Tests calculating all aspects for a set of planets.
    """

    points = create_test_points(
        {"longitude": 0, "declination": 11, "house": 1},
        {"longitude": 5, "declination": -11, "house": 1},
    )

    points_and_event_type = (points, tim_natal.event)
    aspects = calculate_relationships(points_and_event_type, points_and_event_type, True)

    assert len(aspects) is 1
    assert aspects[0].ecliptic_aspect.type == AspectType.conjunction
    assert aspects[0].sign_aspect == AspectType.conjunction
    assert aspects[0].declination_aspect.type == AspectType.contraparallel


