from typing import Tuple

from astro.chart.relationship.phase import calculate_aspect_phase
from astro.schema import RelationshipSchema
from astro.util import PhaseType, Point
from test.utils import create_test_points


def create_phase_points(
        degrees_of_moon: int,
        degrees_of_mercury: int = 0,
        point_name: Point = Point.mercury
) -> RelationshipSchema:
    """
    Creates a relationship with a phase by the given degrees of separation.

    :param degrees_of_moon: The degrees of the moon.
    :param degrees_of_mercury: The degrees of mercury.
    :param point_name: An alternate second point to use, defaulting to Mercury.

    :return: A relationship between the two points with the phase calculated.
    """

    from_point, to_point = create_test_points(
        {"degrees_from_aries": degrees_of_moon, "name": Point.moon},
        {"degrees_from_aries": degrees_of_mercury, "name": point_name},
    )
    relationship = RelationshipSchema(from_point=from_point.name, to_point=to_point.name)

    calculate_aspect_phase(relationship, from_point, to_point)

    return relationship


def create_inferior_phase_points(
        degrees_of_separation: int,
        speed: float
) -> Tuple[RelationshipSchema, RelationshipSchema]:
    """
    Creates relationships between the Sun Venus and Mercury with a phase by the given degrees of separation.

    :param degrees_of_separation: The degrees of the separation.
    :param speed: The speed of Venus and Mercury.

    :return:
        [0] Relationship between the Sun and Venus.
        [1] Relationship between the Sun and Mercury.
    """

    sun, venus, mercury = create_test_points(
        {"degrees_from_aries": degrees_of_separation, "name": Point.sun},
        {"degrees_from_aries": 0, "name": Point.venus, "speed": speed},
        {"degrees_from_aries": 0, "name": Point.mercury, "speed": speed},
    )
    relationship_venus = RelationshipSchema(from_point=sun.name, to_point=venus.name)
    relationship_mercury = RelationshipSchema(from_point=sun.name, to_point=mercury.name)

    calculate_aspect_phase(relationship_venus, sun, venus)
    calculate_aspect_phase(relationship_mercury, sun, mercury)

    return relationship_venus, relationship_mercury


def test_calculate_phase__inferior_new():
    """
    Tests that new phase aspects between the Sun and inferior planets, which
    are unable to make a complete zodiacal cycle relative to the sun,
    are calculated correctly.
    """

    relationship_venus, relationship_mercury = create_inferior_phase_points(10, -0.1)

    assert relationship_venus.phase is PhaseType.new
    assert relationship_mercury.phase is PhaseType.new


def test_calculate_phase__inferior_first_quarter():
    """
    Tests that first quarter phase aspects between the Sun and inferior planets, which
    are unable to make a complete zodiacal cycle relative to the sun,
    are calculated correctly.
    """

    relationship_venus, relationship_mercury = create_inferior_phase_points(10, 0.1)

    assert relationship_venus.phase is PhaseType.first_quarter
    assert relationship_mercury.phase is PhaseType.first_quarter


def test_calculate_phase__inferior_full():
    """
    Tests that full phase aspects between the Sun and inferior planets, which
    are unable to make a complete zodiacal cycle relative to the sun,
    are calculated correctly.
    """

    relationship_venus, relationship_mercury = create_inferior_phase_points(350, 0.1)

    assert relationship_venus.phase is PhaseType.full
    assert relationship_mercury.phase is PhaseType.full


def test_calculate_phase__inferior_last_quarter():
    """
    Tests that last quarter phase aspects between the Sun and inferior planets, which
    are unable to make a complete zodiacal cycle relative to the sun,
    are calculated correctly.
    """

    relationship_venus, relationship_mercury = create_inferior_phase_points(350, -0.1)

    assert relationship_venus.phase is PhaseType.last_quarter
    assert relationship_mercury.phase is PhaseType.last_quarter


def test_calculate_phase__no_speed():
    """
    Tests that points without a known speed dont have their phase calculated.
    """

    relationship = create_phase_points(0, 10, Point.north_mode)

    assert relationship.phase_base_point is None
    assert relationship.arc_ordered == 10
    assert relationship.phase is None


def test_calculate_phase__no_traits():
    """
    Tests that points without any traits dont have their phase calculated.
    """

    relationship = create_phase_points(0, 10, Point.ascendant)

    assert relationship.phase_base_point is None
    assert relationship.arc_ordered == 10
    assert relationship.phase is None


def test_calculate_phase__slower():
    """
    Tests that the slower planet (Mercury) is used as the base for the phase.
    """

    relationship = create_phase_points(0)

    assert relationship.phase_base_point == Point.mercury


def test_calculate_phase__new():
    """
    Tests calculating planets with a new phase between them.
    """

    relationship = create_phase_points(0)

    assert relationship.arc_ordered == 0
    assert relationship.phase == PhaseType.new


def test_calculate_phase__crescent():
    """
    Tests calculating planets with a crescent phase between them.
    """

    relationship = create_phase_points(45)

    assert relationship.arc_ordered == 45
    assert relationship.phase == PhaseType.crescent


def test_calculate_phase__reversed():
    """
    Tests calculating planets with a crescent phase between them,
    but with reversed degrees of separation.
    """

    relationship = create_phase_points(15, 330)

    assert relationship.arc_ordered == 45
    assert relationship.phase == PhaseType.crescent


def test_calculate_phase__first_quarter():
    """
    Tests calculating planets with a first quarter phase between them.
    """

    relationship = create_phase_points(90)

    assert relationship.arc_ordered == 90
    assert relationship.phase == PhaseType.first_quarter


def test_calculate_phase__gibbous():
    """
    Tests calculating planets with a gibbous phase between them.
    """

    relationship = create_phase_points(135)

    assert relationship.arc_ordered == 135
    assert relationship.phase == PhaseType.gibbous


def test_calculate_phase__full():
    """
    Tests calculating planets with a full phase between them.
    """

    relationship = create_phase_points(180)

    assert relationship.arc_ordered == 180
    assert relationship.phase == PhaseType.full


def test_calculate_phase__disseminating():
    """
    Tests calculating planets with a disseminating phase between them.
    """

    relationship = create_phase_points(225)

    assert relationship.arc_ordered == 225
    assert relationship.phase == PhaseType.disseminating


def test_calculate_phase__last_quarter():
    """
    Tests calculating planets with a last quarter phase between them.
    """

    relationship = create_phase_points(270)

    assert relationship.arc_ordered == 270
    assert relationship.phase == PhaseType.last_quarter


def test_calculate_phase__balsamic():
    """
    Tests calculating planets with a balsamic phase between them.
    """

    relationship = create_phase_points(315)

    assert relationship.arc_ordered == 315
    assert relationship.phase == PhaseType.balsamic
