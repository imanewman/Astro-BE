import swisseph as swe

from src.enums import *
from src.models import ZodiacSignCollection, PointTraitsCollection

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
        },
        Point.uranus: {
            "swe_id": swe.URANUS,
            "name": Point.uranus,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.aquarius],
            "exaltation": [ZodiacSign.scorpio],
            "detriment": [ZodiacSign.leo],
            "fall": [ZodiacSign.taurus],
        },
        Point.neptune: {
            "swe_id": swe.NEPTUNE,
            "name": Point.neptune,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.pisces],
            "exaltation": [ZodiacSign.cancer],
            "detriment": [ZodiacSign.virgo],
            "fall": [ZodiacSign.capricorn],
        },
        Point.pluto: {
            "swe_id": swe.PLUTO,
            "name": Point.pluto,
            "category": PointCategory.outer,
            "domicile": [ZodiacSign.scorpio],
            "exaltation": [ZodiacSign.leo],
            "detriment": [ZodiacSign.taurus],
            "fall": [ZodiacSign.aquarius],
        },
    }
})
