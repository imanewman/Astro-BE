import swisseph as swe

from astro.schema import PointTraitsCollection
from astro.util import Point, PointCategory, ZodiacSign, convert_to_degrees

point_traits = PointTraitsCollection(**{
    "points": {
        Point.moon: {
            "swe_id": swe.MOON,
            "name": Point.moon,
            "category": PointCategory.visible,
            "joy": 3,
            "domicile": [ZodiacSign.cancer],
            "exaltation": [ZodiacSign.taurus],
            "detriment": [ZodiacSign.capricorn],
            "fall": [ZodiacSign.scorpio],
            "speed_avg": convert_to_degrees(13, 59, 8),
            "speed_high": convert_to_degrees(16, 30, 0),
            "speed_low": convert_to_degrees(11, 45, 36),
        },
        Point.mercury: {
            "swe_id": swe.MERCURY,
            "name": Point.mercury,
            "category": PointCategory.visible,
            "joy": 1,
            "domicile": [ZodiacSign.gemini, ZodiacSign.virgo],
            "exaltation": [ZodiacSign.virgo],
            "detriment": [ZodiacSign.sagittarius, ZodiacSign.pisces],
            "fall": [ZodiacSign.pisces],
            "speed_avg": convert_to_degrees(1, 23, 0),
            "speed_high": convert_to_degrees(2, 25, 0),
            "speed_low": convert_to_degrees(-1, -30, 0),
        },
        Point.venus: {
            "swe_id": swe.VENUS,
            "name": Point.venus,
            "category": PointCategory.visible,
            "joy": 5,
            "domicile": [ZodiacSign.taurus, ZodiacSign.libra],
            "exaltation": [ZodiacSign.pisces],
            "detriment": [ZodiacSign.aries, ZodiacSign.scorpio],
            "fall": [ZodiacSign.virgo],
            "speed_avg": convert_to_degrees(1, 12, 0),
            "speed_high": convert_to_degrees(1, 22, 0),
            "speed_low": convert_to_degrees(0, -41, -12),
        },
        Point.sun: {
            "swe_id": swe.SUN,
            "name": Point.sun,
            "category": PointCategory.visible,
            "joy": 9,
            "domicile": [ZodiacSign.leo],
            "exaltation": [ZodiacSign.aries],
            "detriment": [ZodiacSign.aquarius],
            "fall": [ZodiacSign.libra],
            "speed_avg": convert_to_degrees(0, 59, 8),
            "speed_high": convert_to_degrees(1, 3, 0),
            "speed_low": convert_to_degrees(0, 57, 10),
        },
        Point.mars: {
            "swe_id": swe.MARS,
            "name": Point.mars,
            "category": PointCategory.visible,
            "joy": 6,
            "domicile": [ZodiacSign.aries, ZodiacSign.scorpio],
            "exaltation": [ZodiacSign.capricorn],
            "detriment": [ZodiacSign.libra, ZodiacSign.taurus],
            "fall": [ZodiacSign.cancer],
            "speed_avg": convert_to_degrees(0, 31, 27),
            "speed_high": convert_to_degrees(0, 52, 0),
            "speed_low": convert_to_degrees(0, -26, -12),
        },
        Point.jupiter: {
            "swe_id": swe.JUPITER,
            "name": Point.jupiter,
            "category": PointCategory.visible,
            "joy": 11,
            "domicile": [ZodiacSign.sagittarius, ZodiacSign.pisces],
            "exaltation": [ZodiacSign.cancer],
            "detriment": [ZodiacSign.gemini, ZodiacSign.virgo],
            "fall": [ZodiacSign.capricorn],
            "speed_avg": convert_to_degrees(0, 4, 59),
            "speed_high": convert_to_degrees(0, 15, 40),
            "speed_low": convert_to_degrees(0, -8, -50),
        },
        Point.saturn: {
            "swe_id": swe.SATURN,
            "name": Point.saturn,
            "category": PointCategory.visible,
            "joy": 12,
            "domicile": [ZodiacSign.capricorn, ZodiacSign.aquarius],
            "exaltation": [ZodiacSign.libra],
            "detriment": [ZodiacSign.cancer, ZodiacSign.leo],
            "fall": [ZodiacSign.aries],
            "speed_avg": convert_to_degrees(0, 2, 1),
            "speed_high": convert_to_degrees(0, 8, 48),
            "speed_low": convert_to_degrees(0, -5, -30),
        },
        Point.uranus: {
            "swe_id": swe.URANUS,
            "name": Point.uranus,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.aquarius],
            "exaltation": [ZodiacSign.scorpio],
            "detriment": [ZodiacSign.leo],
            "fall": [ZodiacSign.taurus],
            "speed_avg": convert_to_degrees(0, 0, 42),
            "speed_high": convert_to_degrees(0, 4, 0),
            "speed_low": convert_to_degrees(0, -2, -40),
        },
        Point.neptune: {
            "swe_id": swe.NEPTUNE,
            "name": Point.neptune,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.pisces],
            "exaltation": [],
            "detriment": [ZodiacSign.virgo],
            "fall": [],
            "speed_avg": convert_to_degrees(0, 0, 24),
            "speed_high": convert_to_degrees(0, 2, 25),
            "speed_low": convert_to_degrees(0, -1, -45),
        },
        Point.pluto: {
            "swe_id": swe.PLUTO,
            "name": Point.pluto,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.scorpio],
            "exaltation": [],
            "detriment": [ZodiacSign.taurus],
            "fall": [],
            "speed_avg": convert_to_degrees(0, 0, 15),
            "speed_high": convert_to_degrees(0, 2, 30),
            "speed_low": convert_to_degrees(0, -1, -48),
        },

        # TODO: these require a path to the swiss ephemeris with their locations
        # Point.chiron: {
        #     "swe_id": swe.CHIRON,
        #     "name": Point.chiron,
        #     "speed_avg": convert_to_degrees(0, 2, 0),
        #     "speed_high": convert_to_degrees(0, 10, 0),
        #     "speed_low": convert_to_degrees(0, -6, 0),
        # },
        # Point.pholus: {
        #     "swe_id": swe.PHOLUS,
        #     "name": Point.pholus,
        # },
        # Point.ceres: {
        #     "swe_id": swe.CERES,
        #     "name": Point.ceres,
        #     "speed_avg": convert_to_degrees(0, 12, 40),
        #     "speed_high": convert_to_degrees(0, 30, 0),
        #     "speed_low": convert_to_degrees(0, -16, 0),
        # },
        # Point.pallas: {
        #     "swe_id": swe.PALLAS,
        #     "name": Point.pallas,
        #     "speed_avg": convert_to_degrees(0, 12, 20),
        #     "speed_high": convert_to_degrees(0, 40, 30),
        #     "speed_low": convert_to_degrees(0, -22, -30),
        # },
        # Point.juno: {
        #     "swe_id": swe.JUNO,
        #     "name": Point.juno,
        #     "speed_avg": convert_to_degrees(0, 14, 15),
        #     "speed_high": convert_to_degrees(0, 39, 0),
        #     "speed_low": convert_to_degrees(0, -18, 0),
        # },
        # Point.vesta: {
        #     "swe_id": swe.VESTA,
        #     "name": Point.vesta,
        #     "speed_avg": convert_to_degrees(0, 16, 15),
        #     "speed_high": convert_to_degrees(0, 36, 0),
        #     "speed_low": convert_to_degrees(0, -17, -32),
        # },
        # Point.psyche: {
        #     "swe_id": None,
        #     "name": Point.psyche,
        # },
        # Point.charklo: {
        #     "swe_id": None,
        #     "name": Point.charklo,
        # },
        # Point.eros: {
        #     "swe_id": None,
        #     "name": Point.eros,
        # },
        # Point.eris: {
        #     "swe_id": None,
        #     "name": Point.eris,
        # },

        Point.north_mode: {
            "swe_id": swe.TRUE_NODE,
            "name": Point.north_mode,
            "category": PointCategory.point,
        },
    }
})
"""
Associates each point with relevant information.

- Planetary joys: https://theastrologydictionary.com/j/joys/
- Essential dignities: https://www.astro.com/astrowiki/en/Domicile, 
  https://astrostyle.com/the-essential-dignities-of-planets-exalted-detriment-domicile-and-fall/, 
  https://www.into-it.com/blog/outerplanetdignities
  - outer planets are missing debated dignities
- Speeds: https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/
"""