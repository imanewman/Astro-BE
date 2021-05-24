import swisseph as swe

from astro.schema.point import PointTraitsCollection
from astro.schema.sign import ZodiacSignCollection
from .enums import *
from .functions import convert_to_degrees
from ..chart import get_julian_day
from ..schema import DateTimeLocation
from ..schema.aspect import AspectTraitsCollection

"""
Exports the traditional order of zodiac signs.
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
Associates each zodiac sign with relevant information.

- Reference for essential dignities: 
    https://theastrologypodcast.com/wp-content/uploads/2018/05/essential-dignities-table-large.jpg
"""
zodiac_sign_traits = ZodiacSignCollection(**{
    "signs": {
        ZodiacSign.aries: {
            "sign": ZodiacSign.aries,
            "polarity": Polarity.yang,
            "modality": Modality.cardinal,
            "element": Element.fire,
            "rulership": Point.mars,
            "exaltation": Point.sun,
            "triplicity": [Point.sun, Point.jupiter, Point.saturn],
            "bounds": [
                {"ruler": Point.jupiter, "from_degree": 0, "to_degree": 6},
                {"ruler": Point.venus, "from_degree": 6, "to_degree": 12},
                {"ruler": Point.mercury, "from_degree": 12, "to_degree": 20},
                {"ruler": Point.mars, "from_degree": 20, "to_degree": 25},
                {"ruler": Point.saturn, "from_degree": 25, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.mars, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.sun, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.venus, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.venus,
            "fall": Point.saturn,
        },
        ZodiacSign.taurus: {
            "sign": ZodiacSign.taurus,
            "polarity": Polarity.yin,
            "modality": Modality.fixed,
            "element": Element.earth,
            "rulership": Point.venus,
            "exaltation": Point.moon,
            "triplicity": [Point.venus, Point.moon, Point.mars],
            "bounds": [
                {"ruler": Point.venus, "from_degree": 0, "to_degree": 8},
                {"ruler": Point.mercury, "from_degree": 8, "to_degree": 14},
                {"ruler": Point.jupiter, "from_degree": 14, "to_degree": 22},
                {"ruler": Point.saturn, "from_degree": 22, "to_degree": 27},
                {"ruler": Point.mars, "from_degree": 27, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.mercury, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.moon, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.saturn, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.mars,
            "fall": None,
        },
        ZodiacSign.gemini: {
            "sign": ZodiacSign.gemini,
            "polarity": Polarity.yang,
            "modality": Modality.mutable,
            "element": Element.air,
            "rulership": Point.mercury,
            "exaltation": None,
            "triplicity": [Point.saturn, Point.mercury, Point.jupiter],
            "bounds": [
                {"ruler": Point.mercury, "from_degree": 0, "to_degree": 6},
                {"ruler": Point.jupiter, "from_degree": 6, "to_degree": 12},
                {"ruler": Point.venus, "from_degree": 12, "to_degree": 17},
                {"ruler": Point.mars, "from_degree": 17, "to_degree": 24},
                {"ruler": Point.saturn, "from_degree": 24, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.jupiter, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.mars, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.sun, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.jupiter,
            "fall": None,
        },
        ZodiacSign.cancer: {
            "sign": ZodiacSign.cancer,
            "polarity": Polarity.yin,
            "modality": Modality.cardinal,
            "element": Element.water,
            "rulership": Point.moon,
            "exaltation": Point.jupiter,
            "triplicity": [Point.venus, Point.mars, Point.moon],
            "bounds": [
                {"ruler": Point.mars, "from_degree": 0, "to_degree": 7},
                {"ruler": Point.venus, "from_degree": 7, "to_degree": 13},
                {"ruler": Point.mercury, "from_degree": 13, "to_degree": 19},
                {"ruler": Point.jupiter, "from_degree": 19, "to_degree": 26},
                {"ruler": Point.saturn, "from_degree": 26, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.venus, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.mercury, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.moon, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.saturn,
            "fall": Point.mars,
        },
        ZodiacSign.leo: {
            "sign": ZodiacSign.leo,
            "polarity": Polarity.yang,
            "modality": Modality.fixed,
            "element": Element.fire,
            "rulership": Point.sun,
            "exaltation": None,
            "triplicity": [Point.sun, Point.jupiter, Point.saturn],
            "bounds": [
                {"ruler": Point.jupiter, "from_degree": 0, "to_degree": 7},
                {"ruler": Point.venus, "from_degree": 7, "to_degree": 13},
                {"ruler": Point.saturn, "from_degree": 13, "to_degree": 19},
                {"ruler": Point.mercury, "from_degree": 19, "to_degree": 26},
                {"ruler": Point.mars, "from_degree": 26, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.saturn, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.jupiter, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.mars, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.saturn,
            "fall": None,
        },
        ZodiacSign.virgo: {
            "sign": ZodiacSign.virgo,
            "polarity": Polarity.yin,
            "modality": Modality.mutable,
            "element": Element.earth,
            "rulership": Point.mercury,
            "exaltation": Point.mercury,
            "triplicity": [Point.mercury, Point.moon, Point.mars],
            "bounds": [
                {"ruler": Point.mercury, "from_degree": 0, "to_degree": 7},
                {"ruler": Point.venus, "from_degree": 7, "to_degree": 17},
                {"ruler": Point.jupiter, "from_degree": 17, "to_degree": 21},
                {"ruler": Point.mars, "from_degree": 21, "to_degree": 28},
                {"ruler": Point.saturn, "from_degree": 28, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.sun, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.venus, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.mercury, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.jupiter,
            "fall": Point.venus,
        },
        ZodiacSign.libra: {
            "sign": ZodiacSign.libra,
            "polarity": Polarity.yang,
            "modality": Modality.cardinal,
            "element": Element.air,
            "rulership": Point.venus,
            "exaltation": Point.saturn,
            "triplicity": [Point.saturn, Point.mercury, Point.jupiter],
            "bounds": [
                {"ruler": Point.saturn, "from_degree": 0, "to_degree": 6},
                {"ruler": Point.mercury, "from_degree": 6, "to_degree": 14},
                {"ruler": Point.jupiter, "from_degree": 14, "to_degree": 21},
                {"ruler": Point.venus, "from_degree": 21, "to_degree": 28},
                {"ruler": Point.mars, "from_degree": 28, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.moon, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.saturn, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.jupiter, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.mars,
            "fall": Point.sun,
        },
        ZodiacSign.scorpio: {
            "sign": ZodiacSign.scorpio,
            "polarity": Polarity.yin,
            "modality": Modality.fixed,
            "element": Element.water,
            "rulership": Point.mars,
            "exaltation": None,
            "triplicity": [Point.venus, Point.mars, Point.moon],
            "bounds": [
                {"ruler": Point.mars, "from_degree": 0, "to_degree": 7},
                {"ruler": Point.venus, "from_degree": 7, "to_degree": 11},
                {"ruler": Point.mercury, "from_degree": 11, "to_degree": 19},
                {"ruler": Point.jupiter, "from_degree": 19, "to_degree": 24},
                {"ruler": Point.saturn, "from_degree": 24, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.mars, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.sun, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.venus, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.venus,
            "fall": Point.moon,
        },
        ZodiacSign.sagittarius: {
            "sign": ZodiacSign.sagittarius,
            "polarity": Polarity.yang,
            "modality": Modality.mutable,
            "element": Element.fire,
            "rulership": Point.jupiter,
            "exaltation": None,
            "triplicity": [Point.sun, Point.jupiter, Point.saturn],
            "bounds": [
                {"ruler": Point.jupiter, "from_degree": 0, "to_degree": 12},
                {"ruler": Point.venus, "from_degree": 12, "to_degree": 17},
                {"ruler": Point.mercury, "from_degree": 17, "to_degree": 21},
                {"ruler": Point.saturn, "from_degree": 21, "to_degree": 26},
                {"ruler": Point.mars, "from_degree": 26, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.mercury, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.moon, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.saturn, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.mercury,
            "fall": None,
        },
        ZodiacSign.capricorn: {
            "sign": ZodiacSign.capricorn,
            "polarity": Polarity.yin,
            "modality": Modality.cardinal,
            "element": Element.earth,
            "rulership": Point.saturn,
            "exaltation": Point.mars,
            "triplicity": [Point.venus, Point.moon, Point.mars],
            "bounds": [
                {"ruler": Point.mercury, "from_degree": 0, "to_degree": 12},
                {"ruler": Point.jupiter, "from_degree": 12, "to_degree": 17},
                {"ruler": Point.venus, "from_degree": 17, "to_degree": 21},
                {"ruler": Point.saturn, "from_degree": 21, "to_degree": 26},
                {"ruler": Point.mars, "from_degree": 26, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.jupiter, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.mars, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.sun, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.moon,
            "fall": Point.jupiter,
        },
        ZodiacSign.aquarius: {
            "sign": ZodiacSign.aquarius,
            "polarity": Polarity.yang,
            "modality": Modality.fixed,
            "element": Element.air,
            "rulership": Point.saturn,
            "exaltation": None,
            "triplicity": [Point.saturn, Point.mercury, Point.jupiter],
            "bounds": [
                {"ruler": Point.mercury, "from_degree": 0, "to_degree": 7},
                {"ruler": Point.venus, "from_degree": 7, "to_degree": 13},
                {"ruler": Point.jupiter, "from_degree": 13, "to_degree": 20},
                {"ruler": Point.mars, "from_degree": 20, "to_degree": 25},
                {"ruler": Point.saturn, "from_degree": 25, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.venus, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.mercury, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.moon, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.sun,
            "fall": None,
        },
        ZodiacSign.pisces: {
            "sign": ZodiacSign.pisces,
            "polarity": Polarity.yin,
            "modality": Modality.mutable,
            "element": Element.water,
            "rulership": Point.jupiter,
            "exaltation": Point.venus,
            "triplicity": [Point.venus, Point.mars, Point.moon],
            "bounds": [
                {"ruler": Point.venus, "from_degree": 0, "to_degree": 12},
                {"ruler": Point.jupiter, "from_degree": 12, "to_degree": 16},
                {"ruler": Point.mercury, "from_degree": 16, "to_degree": 19},
                {"ruler": Point.mars, "from_degree": 19, "to_degree": 28},
                {"ruler": Point.saturn, "from_degree": 28, "to_degree": 30},
            ],
            "decans": [
                {"ruler": Point.saturn, "from_degree": 0, "to_degree": 10},
                {"ruler": Point.jupiter, "from_degree": 10, "to_degree": 20},
                {"ruler": Point.mars, "from_degree": 20, "to_degree": 30},
            ],
            "detriment": Point.mercury,
            "fall": None,
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
            "swe_id": swe.MEAN_NODE,
            "name": Point.north_mode,
            "category": PointCategory.point,
        },
    }
})

"""
Associates each aspect with the degrees associated with it.
"""
aspectTraits = AspectTraitsCollection(**{
    "aspects": {
        AspectType.conjunction: {
            "name": AspectType.conjunction,
            "degrees": 0,
        },
        AspectType.opposition: {
            "name": AspectType.opposition,
            "degrees": 180,
        },
        AspectType.square: {
            "name": AspectType.square,
            "degrees": 90,
        },
        AspectType.trine: {
            "name": AspectType.trine,
            "degrees": 120,
        },
        AspectType.sextile: {
            "name": AspectType.sextile,
            "degrees": 60,
        },
        AspectType.quintile: {
            "name": AspectType.quintile,
            "degrees": 72,
        },
        AspectType.septile: {
            "name": AspectType.septile,
            "degrees": 51,
        },
        AspectType.octile: {
            "name": AspectType.octile,
            "degrees": 45,
        },
        AspectType.novile: {
            "name": AspectType.novile,
            "degrees": 40,
        },
        AspectType.semi_sextile: {
            "name": AspectType.semi_sextile,
            "degrees": 30,
        },
        AspectType.quincunx: {
            "name": AspectType.quincunx,
            "degrees": 150,
        },
        AspectType.sesquiquadrate: {
            "name": AspectType.sesquiquadrate,
            "degrees": 135,
        },
        AspectType.bi_quintile: {
            "name": AspectType.bi_quintile,
            "degrees": 144,
        },
    }
})


"""
The date time of Tim's birth.
"""
tim_natal = DateTimeLocation(
    date="1997-10-11T15:09:00.000Z",
    latitude=40.78343,
    longitude=-73.96625,
)

tim_natal.julian_day = get_julian_day(tim_natal.date)
