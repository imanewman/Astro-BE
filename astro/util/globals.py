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

modern_points = [
    *traditional_points,
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

default_enabled_points = [
    *calculated_points,
    *modern_points,
    *primary_asteroid_points,
    Point.north_mode,
]
"""
Defines the list of points enabled for calculations by default.
"""

major_aspects = [
    AspectType.conjunction,
    AspectType.opposition,
    AspectType.trine,
    AspectType.square,
    AspectType.sextile,
    AspectType.parallel,
    AspectType.contraparallel,
]
"""
Defines all major aspects.
"""

fifth_harmonic_aspects = [
    AspectType.quintile,
    AspectType.bi_quintile,
]

seventh_harmonic_aspects = [
    AspectType.septile,
    AspectType.bi_septile,
    AspectType.tri_septile,
]

eighth_harmonic_aspects = [
    AspectType.octile,
    AspectType.sesquiquadrate,
]

ninth_harmonic_aspects = [
    AspectType.novile,
    AspectType.bi_novile,
    AspectType.quadri_novile,
]

twelfth_harmonic_aspects = [
    AspectType.semi_sextile,
    AspectType.quincunx,
]

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
    # *minor_aspects,
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


modern_midpoints = calculate_midpoints(modern_points)
"""
Defines a list of all midpoints between modern planets.
"""