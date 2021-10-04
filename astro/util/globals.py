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
]
"""
Defines the list of points enabled for calculations by default.
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