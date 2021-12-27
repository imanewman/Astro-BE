from typing import List, Tuple, Dict

from astro.schema import PointSchema, RelationshipSchema, SettingsSchema, EventSettingsSchema, EventSchema, \
    EnabledPointsSettingsSchema
from .declination_aspect import calculate_declination_aspect
from .ecliptic_aspect import calculate_ecliptic_aspect
from .aspect_movement import calculate_aspect_movement
from .phase import calculate_aspect_phase
from .sign_aspect import calculate_sign_aspect
from astro.util import AspectSortType, do_points_form_axis


def calculate_relationships(
        from_items: Tuple[List[PointSchema], EventSettingsSchema],
        to_items: Tuple[List[PointSchema], EventSettingsSchema],
        is_one_chart: bool = False,
        settings: SettingsSchema = SettingsSchema()
) -> List[RelationshipSchema]:
    """
    Calculates the relationships between each set of 2 points.

    - By default, orbs and allowed aspects are decided by the event with
      the highest priority (enabled point index) of enabled aspects.

    :param from_items: The points to calculate aspects from, and the event.
    :param to_items: The points to calculate aspects to, and the event.
    :param is_one_chart: If true, aspects will not be bi-directionally duplicated.
    :param settings: The settings to use for calculations.

    :return: All calculated relationships.
    """
    from_points, from_event = from_items
    to_points, to_event = to_items
    precession_correction = calculate_precession_correction_degrees(
        from_event.event, to_event.event)
    relationships = []

    for from_point in from_points:
        if is_one_chart:
            # Skip the points that have been calculated already to avoid duplicates.
            to_points = to_points[1:]

        for to_point in to_points:
            to_enabled, to_priority = to_event.get_enabled_for_point(to_point)
            from_enabled, from_priority = from_event.get_enabled_for_point(from_point)

            if from_priority is None or to_priority >= from_priority:
                enabled_settings = to_enabled
            else:
                enabled_settings = from_enabled

            relationships.append(create_relationship(
                (from_point, from_event),
                (to_point, to_event),
                is_one_chart,
                precession_correction,
                enabled_settings
            ))

    sort_relationships(relationships, settings.aspect_sort)

    return relationships


def sort_relationships(relationships: List[RelationshipSchema], aspect_sort: AspectSortType):
    """
    Sorts the relationships by whatever aspect sort type is set.

    :param relationships: The relationships to sort.
    :param aspect_sort: The sort type to run.
    """
    if aspect_sort == AspectSortType.smallest_orb:
        # Sort ordered by the smallest orb.
        def sort_smallest_orb(rel: RelationshipSchema) -> float:
            aspect_orbs = map(
                lambda aspect: abs(aspect.orb or 360),
                rel.get_applying_aspects()
            )

            return min(aspect_orbs, default=360)

        relationships.sort(key=sort_smallest_orb)

    elif aspect_sort == AspectSortType.closest_exact:
        # Sort ordered by the closest exact aspect.
        def sort_closest_exact(rel: RelationshipSchema) -> float:
            aspect_orbs = map(
                lambda aspect: abs(aspect.days_until_exact or 7),
                rel.get_applying_aspects()
            )

            return min(aspect_orbs, default=7)

        relationships.sort(key=sort_closest_exact)


def create_relationship(
        from_item: Tuple[PointSchema, EventSettingsSchema],
        to_item: Tuple[PointSchema, EventSettingsSchema],
        is_one_chart: bool,
        precession_correction: float = 0,
        enabled_settings: EnabledPointsSettingsSchema() = EnabledPointsSettingsSchema()
) -> RelationshipSchema:
    """
    Creates a relationship object, initializing all internal values.

    :param from_item: The starting point in the relationship, and the event it is from.
    :param to_item: The ending point in the relationship, and the event it is from.
    :param is_one_chart: If true, aspects will not be bi-directionally duplicated.
    :param precession_correction: The degrees of precession correction between events.
    :param enabled_settings: The settings to use for calculations.

    :return: The created relationship.
    """
    from_point, from_event = from_item
    to_point, to_event = to_item

    relationship = RelationshipSchema(
        from_point=from_point.name,
        to_point=to_point.name,
        precession_correction=precession_correction
    )

    calculate_sign_aspect(relationship, from_point, to_point)

    if not is_one_chart or not do_points_form_axis(from_point.name, to_point.name):
        # Skip calculations for aspects that form an axis in the same chart.
        calculate_ecliptic_aspect(relationship, from_point, to_point, enabled_settings)
        calculate_aspect_phase(relationship, from_point, to_point)
        calculate_declination_aspect(relationship, from_point, to_point, enabled_settings)
        calculate_aspect_movement(
            relationship,
            (from_point, from_event.event),
            (to_point, to_event.event)
        )

    return relationship


def calculate_precession_correction_degrees(from_event: EventSchema, to_event: EventSchema) -> float:
    """
    Calculates the precession correction degrees to the `from_event` that standardizes its location
    to the `to_event`. This accounts for the vernal equinox slowly precessing backwards over time.

    :param from_event: The starting event.
    :param to_event: The ending event.

    :return: The degrees to add to all locations in the starting event to more accurately compare them
             to the ending event.
    """
    date_difference = to_event.utc_date - from_event.utc_date
    date_difference_in_years = date_difference.days / 365
    precession_correction_degrees_per_year = 50.25 / 60 / 60
    precession_correction_degrees = date_difference_in_years * precession_correction_degrees_per_year

    return precession_correction_degrees
