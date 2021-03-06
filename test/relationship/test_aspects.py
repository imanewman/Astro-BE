from astro import calculate_relationships
from astro.chart import calculate_precession_correction_degrees
from astro.schema import EventSchema, EventSettingsSchema
from astro.util import AspectType, EventType
from astro.util.test_events import tim_natal
from test.utils import create_test_points


def test_calculate_aspects():
    """
    Tests calculating all aspects for a set of planets.
    """

    points = create_test_points(
        {"longitude": 0, "declination": 11, "house": 1},
        {"longitude": 5, "declination": -11, "house": 1},
        do_init_point=True
    )

    points_and_event_type = (points, tim_natal)
    aspects = calculate_relationships(points_and_event_type, points_and_event_type, True)

    assert len(aspects) is 1
    assert aspects[0].ecliptic_aspect.type == AspectType.conjunction
    assert aspects[0].sign_aspect == AspectType.conjunction
    assert aspects[0].declination_aspect.type == AspectType.contraparallel
    assert aspects[0].precession_correction == 0


def test_calculate_precession_correction_degrees():
    """
    Tests calculating the precession correction orb.
    """

    precession_correction = calculate_precession_correction_degrees(
        EventSchema(
            utc_date="2026-12-12T00:00:00.000Z"
        ),
        EventSchema(
            utc_date="2028-12-12T00:00:00.000Z"
        ),
    )

    assert abs(precession_correction - 100.5 / 60 / 60) < 0.01


def test_calculate_multiple_aspect_sets():
    """
    Tests calculating all aspects between sets of points with different enabled aspects.
    """

    points = create_test_points({"longitude": 0}, do_init_point=True)

    aspects = calculate_relationships(
        (points, EventSettingsSchema(event=tim_natal)),
        (points, EventSettingsSchema(
            event=tim_natal,
            enabled=[{"points": []}, {"aspects": []}]
        )),
        False
    )

    assert len(aspects) is 1
    assert aspects[0].ecliptic_aspect.type is None
    assert aspects[0].sign_aspect == AspectType.conjunction
