from .enums import *
from .midpoints import calculate_midpoints

calculated_points = [
    Point.ascendant,
    Point.midheaven,
    Point.descendant,
    Point.inner_heaven,
    Point.vertex,
]
"""
Defines points calculated by time of day.
"""

traditional_points = [
    Point.moon,
    Point.mercury,
    Point.venus,
    Point.sun,
    Point.mars,
    Point.jupiter,
    Point.saturn,
]
"""
Defines traditional planets.
"""

lunar_nodes = [
    Point.north_mode,
    Point.south_node
]
"""
Defines the lunar nodes
"""

modern_points = [
    Point.uranus,
    Point.neptune,
    Point.pluto,
]
"""
Defines modern planets.
"""

centaur_points = [
    Point.chiron,
    Point.pholus,
    Point.charklo,
]
"""
Defines centaurs.
"""

primary_asteroid_points = [
    Point.ceres,
    Point.pallas,
    Point.juno,
    Point.vesta,
]
"""
Defines common asteroids.
"""

secondary_asteroid_points = [
    Point.psyche,
    Point.eros,
    Point.lilith,
    Point.toro,
    Point.sappho,
    Point.amor,
    Point.pandora,
    Point.icarus,
    Point.diana,
    Point.hidalgo,
    Point.urania,
    Point.eris,
]
"""
Defines uncommon asteroids.
"""

lot_points = [
    Point.lot_of_fortune,
    Point.lot_of_spirit,
    Point.lot_of_necessity,
    Point.lot_of_eros,
    Point.lot_of_courage,
    Point.lot_of_victory,
    Point.lot_of_nemesis,
]
"""
Defines a list of all midpoints between modern planets.
"""

default_enabled_points = [
    *calculated_points,
    *traditional_points,
    *lunar_nodes,
    *modern_points,
    *primary_asteroid_points,
    Point.lot_of_fortune,
    Point.lot_of_spirit,
]
"""
Defines the list of points enabled for calculations by default.
"""

hard_major_aspects = [
    AspectType.conjunction,
    AspectType.opposition,
    AspectType.square,
]
"""
Defines major hard aspects.
"""

soft_major_aspects = [
    AspectType.trine,
    AspectType.sextile,
]
"""
Defines major soft aspects.
"""

major_aspects = [
    *hard_major_aspects,
    *soft_major_aspects,
]
"""
Defines all major aspects.
"""

fifth_harmonic_aspects = [
    AspectType.quintile,
    AspectType.bi_quintile,
]
"""
Defines 5th harmonic aspects.
"""

seventh_harmonic_aspects = [
    AspectType.septile,
    AspectType.bi_septile,
    AspectType.tri_septile,
]
"""
Defines 7th harmonic aspects.
"""

eighth_harmonic_aspects = [
    AspectType.octile,
    AspectType.sesquiquadrate,
]
"""
Defines 8th harmonic aspects.
"""

ninth_harmonic_aspects = [
    AspectType.novile,
    AspectType.bi_novile,
    AspectType.quadri_novile,
]
"""
Defines 9th harmonic aspects.
"""

twelfth_harmonic_aspects = [
    AspectType.semi_sextile,
    AspectType.quincunx,
]
"""
Defines 12th harmonic aspects.
"""

minor_aspects = [
    *fifth_harmonic_aspects,
    *seventh_harmonic_aspects,
    *eighth_harmonic_aspects,
    *ninth_harmonic_aspects,
    *twelfth_harmonic_aspects,
]
"""
Defines all minor aspects.
"""

declination_aspects = [
    AspectType.parallel,
    AspectType.contraparallel,
]
"""
Defines all declination aspects.
"""

all_aspects = [
    *major_aspects,
    *minor_aspects,
    *declination_aspects,
]
"""
Defines all aspects.
"""

default_enabled_aspects = [
    *major_aspects,
    *eighth_harmonic_aspects,
    *declination_aspects,
]
"""
Defines the list of aspects enabled for calculations by default.
"""

zodiac_sign_order = [
    ZodiacSign.aries,
    ZodiacSign.taurus,
    ZodiacSign.gemini,
    ZodiacSign.cancer,
    ZodiacSign.leo,
    ZodiacSign.virgo,
    ZodiacSign.libra,
    ZodiacSign.scorpio,
    ZodiacSign.sagittarius,
    ZodiacSign.capricorn,
    ZodiacSign.aquarius,
    ZodiacSign.pisces
]
"""
Defines the traditional order of zodiac signs.
"""

point_axis_list = [
    [Point.north_mode, Point.south_node],
    [Point.ascendant, Point.descendant],
    [Point.midheaven, Point.inner_heaven],
]
"""
Defines a list of all points that always form an axis.
"""

default_midpoints = calculate_midpoints([
    *traditional_points,
    *modern_points,
    Point.chiron,
])
"""
Defines a list of all midpoints between modern planets.
"""