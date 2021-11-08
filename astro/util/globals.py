from .enums import *

default_enabled_points = [
    Point.ascendant,
    Point.midheaven,
    Point.descendant,
    Point.inner_heaven,
    Point.vertex,

    Point.moon,
    Point.mercury,
    Point.venus,
    Point.sun,
    Point.mars,
    Point.jupiter,
    Point.saturn,
    Point.uranus,
    Point.neptune,
    Point.pluto,

    Point.north_mode,

    Point.chiron,
    Point.pholus,
    Point.charklo,

    Point.ceres,
    Point.pallas,
    Point.juno,
    Point.vesta,

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

minor_aspects = [
    AspectType.quintile,
    AspectType.septile,
    AspectType.octile,
    AspectType.novile,
    AspectType.semi_sextile,
    AspectType.quincunx,
    AspectType.sesquiquadrate,
    AspectType.bi_quintile,
]
"""
Defines all minor aspects.
"""

default_enabled_aspects = [
    AspectType.conjunction,
    AspectType.opposition,
    AspectType.trine,
    AspectType.square,
    AspectType.sextile,

    AspectType.quintile,
    AspectType.septile,
    AspectType.octile,
    AspectType.novile,
    AspectType.semi_sextile,
    AspectType.quincunx,
    AspectType.sesquiquadrate,
    AspectType.bi_quintile,

    AspectType.parallel,
    AspectType.contraparallel,
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
Exports the traditional order of zodiac signs.
"""

point_axis_list = [
    [Point.north_mode, Point.south_node],
    [Point.ascendant, Point.descendant],
    [Point.midheaven, Point.inner_heaven],
]
"""
Defines a list of all points that always form an axis.
"""