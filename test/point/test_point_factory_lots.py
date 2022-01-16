from astro import create_points_with_attributes
from astro.chart.point.lot_factory import create_lot
from astro.schema import EventSettingsSchema
from astro.util import Point
from astro.util.test_events import tim_natal


def test_create_invalid_lot():
    """
    Tests creating an invalid lot.
    """
    points = create_points_with_attributes(tim_natal)

    assert create_lot(points, Point.sun, True) is None

    points = create_points_with_attributes(EventSettingsSchema(event=tim_natal.event, enabled=[]))

    assert create_lot(points, Point.lot_of_fortune, True) is None


def test_create_lot_of_fortune():
    """
    Tests creating the lot of fortune at day time.
    """
    points = create_points_with_attributes(tim_natal)
    lot = create_lot(points, Point.lot_of_fortune, True)

    assert lot.name == Point.lot_of_fortune
    assert int(lot.longitude) == 3


def test_create_lot_of_fortune__night():
    """
    Tests creating the lot of fortune at night time.
    """
    points = create_points_with_attributes(tim_natal)
    lot = create_lot(points, Point.lot_of_fortune, False)

    assert lot.name == Point.lot_of_fortune
    assert int(lot.longitude) == 128
