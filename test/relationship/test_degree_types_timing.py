from astro.chart.relationship.aspect_movement import calculate_degree_types_timing
from astro.schema import EventSchema, AspectSchema
from astro.util import EventType


def test_calculate_degree_types_timing__none():
    """
    Tests calculating the timing of an aspect more than 7 days in the future.
    """
    aspect = AspectSchema()
    event = EventSchema(
        type=EventType.event,
        local_date="2028-12-12T00:00:00.000Z",
        utc_date="2028-12-12T07:00:00.000Z",
    )

    calculate_degree_types_timing(
        aspect,
        (1, event),
        (1, event),
        1
    )

    assert aspect.days_until_exact is None


def test_calculate_degree_types_timing__this_hour():
    """
    Tests calculating the timing of an aspect going exact within an hour.
    """
    aspect = AspectSchema()
    event = EventSchema(
        type=EventType.event,
        local_date="2028-12-12T00:00:00.000Z",
        utc_date="2028-12-12T07:00:00.000Z",
    )

    calculate_degree_types_timing(
        aspect,
        (24, event),
        (0, event),
        1
    )

    assert aspect.days_until_exact == 1 / 24
    assert str(aspect.utc_date_of_exact) == "2028-12-12 08:00:00+00:00"
    assert str(aspect.local_date_of_exact) == "2028-12-12 01:00:00+00:00"
