from astro import calculate_condition
from astro.util import Point, SectPlacement
from test.utils import create_test_points


def test_calculate_condition():
    """
    Tests calculating the complete condition of a planet.
    """
    moon, sun = create_test_points(
        {"degrees_from_aries": 40, "house": 3},
        {"degrees_from_aries": 40, "name": Point.sun},
        do_init_point=True
    )

    calculate_condition({
        Point.moon: moon,
        Point.sun: sun,
    }, False)

    assert moon.condition.in_joy is True
    assert moon.condition.in_exaltation is True
    assert moon.condition.sect_placement == SectPlacement.sect_light
    assert moon.condition.in_triplicity is True
    assert moon.condition.in_decan is True
    assert moon.condition.is_cazimi is True







