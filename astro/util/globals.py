import swisseph as swe

from astro.schema.point import PointTraitsCollection
from astro.schema.sign import ZodiacSignCollection
from .enums import *
from .functions import convert_to_degrees

"""
Exports the traditional order of zodiac signs.
"""
zodiacSignOrder = [
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
Associates each zodiac sign with relevant information.

- Reference for essential dignities: https://www.astro.com/astrowiki/en/Essential_Dignities
- Reference for decans: https://www.astro.com/astrowiki/en/Face
"""
zodiacSignTraits = ZodiacSignCollection(**{
    "signs": {
        ZodiacSign.aries: {
            "sign": ZodiacSign.aries,
            "polarity": Polarity.yang,
            "modality": Modality.cardinal,
            "element": Element.fire,
            "rulership": Point.mars,
            "decans": [Point.mars, Point.sun, Point.venus]
        },
        ZodiacSign.taurus: {
            "sign": ZodiacSign.taurus,
            "polarity": Polarity.yin,
            "modality": Modality.fixed,
            "element": Element.earth,
            "rulership": Point.venus,
            "decans": [Point.mercury, Point.moon, Point.saturn],
        },
        ZodiacSign.gemini: {
            "sign": ZodiacSign.gemini,
            "polarity": Polarity.yang,
            "modality": Modality.mutable,
            "element": Element.air,
            "rulership": Point.mercury,
            "decans": [Point.jupiter, Point.mars, Point.sun],
        },
        ZodiacSign.cancer: {
            "sign": ZodiacSign.cancer,
            "polarity": Polarity.yin,
            "modality": Modality.cardinal,
            "element": Element.water,
            "rulership": Point.moon,
            "decans": [Point.venus, Point.mercury, Point.moon],
        },
        ZodiacSign.leo: {
            "sign": ZodiacSign.leo,
            "polarity": Polarity.yang,
            "modality": Modality.fixed,
            "element": Element.fire,
            "rulership": Point.sun,
            "decans": [Point.saturn, Point.jupiter, Point.mars],
        },
        ZodiacSign.virgo: {
            "sign": ZodiacSign.virgo,
            "polarity": Polarity.yin,
            "modality": Modality.mutable,
            "element": Element.earth,
            "rulership": Point.mercury,
            "decans": [Point.sun, Point.venus, Point.mercury],
        },
        ZodiacSign.libra: {
            "sign": ZodiacSign.libra,
            "polarity": Polarity.yang,
            "modality": Modality.cardinal,
            "element": Element.air,
            "rulership": Point.venus,
            "decans": [Point.moon, Point.saturn, Point.jupiter],
        },
        ZodiacSign.scorpio: {
            "sign": ZodiacSign.scorpio,
            "polarity": Polarity.yin,
            "modality": Modality.fixed,
            "element": Element.water,
            "rulership": Point.mars,
            "decans": [Point.mars, Point.sun, Point.venus],
        },
        ZodiacSign.sagittarius: {
            "sign": ZodiacSign.sagittarius,
            "polarity": Polarity.yang,
            "modality": Modality.mutable,
            "element": Element.fire,
            "rulership": Point.jupiter,
            "decans": [Point.mercury, Point.moon, Point.saturn],
        },
        ZodiacSign.capricorn: {
            "sign": ZodiacSign.capricorn,
            "polarity": Polarity.yin,
            "modality": Modality.cardinal,
            "element": Element.earth,
            "rulership": Point.saturn,
            "decans": [Point.jupiter, Point.mars, Point.sun],
        },
        ZodiacSign.aquarius: {
            "sign": ZodiacSign.aquarius,
            "polarity": Polarity.yang,
            "modality": Modality.fixed,
            "element": Element.air,
            "rulership": Point.saturn,
            "decans": [Point.venus, Point.mercury, Point.moon],
        },
        ZodiacSign.pisces: {
            "sign": ZodiacSign.pisces,
            "polarity": Polarity.yin,
            "modality": Modality.mutable,
            "element": Element.water,
            "rulership": Point.jupiter,
            "decans": [Point.saturn, Point.jupiter, Point.mars],
        },
    }
})

"""
Associates each point with relevant information.

- Planetary joys: https://theastrologydictionary.com/j/joys/
- Domiciles: https://www.astro.com/astrowiki/en/Domicile
  - Domicile (at home) and exaltation (a welcome guest) are like constructive interference,
    the sign and the planets have archetypal harmony which empowers the planet.
  - Detriment and fall are like deconstructive interference, not necessarily bad but
    there is more need for balancing their conflicting archetypal perspectives.
- Speeds: https://www.celestialinsight.com.au/2020/05/18/when-time-stands-still-exploring-stationary-planets/
    - Uses 30% of average speed to determine stationing.
"""
pointTraits = PointTraitsCollection(**{
    "points": {
        Point.moon: {
            "swe_id": swe.MOON,
            "name": Point.moon,
            "category": PointCategory.visible,
            "joy": 3,
            "domicile": [ZodiacSign.cancer],
            "exaltation": [ZodiacSign.taurus],
            "detriment": [ZodiacSign.capricorn],
            "fall": [ZodiacSign.libra],
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
            "exaltation": [],
            "detriment": [ZodiacSign.sagittarius],
            "fall": [],
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
            "exaltation": [ZodiacSign.cancer],
            "detriment": [ZodiacSign.virgo],
            "fall": [ZodiacSign.capricorn],
            "speed_avg": convert_to_degrees(0, 0, 24),
            "speed_high": convert_to_degrees(0, 2, 25),
            "speed_low": convert_to_degrees(0, -1, -45),
        },
        Point.pluto: {
            "swe_id": swe.PLUTO,
            "name": Point.pluto,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.scorpio],
            "exaltation": [ZodiacSign.leo],
            "detriment": [ZodiacSign.taurus],
            "fall": [ZodiacSign.aquarius],
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

        Point.north_mode: {
            "swe_id": swe.MEAN_NODE,
            "name": Point.north_mode,
            "category": PointCategory.point,
        },
    }
})
