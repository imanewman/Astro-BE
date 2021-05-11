

import swisseph as swe

from src.enums import *
from src.models import ZodiacSignCollection, PointTraitsCollection


# Associates each zodiac sign with relevant information.
# Reference for essential dignities: https://www.astro.com/astrowiki/en/Essential_Dignities
# Reference for decans: https://www.astro.com/astrowiki/en/Face
zodiacSignTraits = ZodiacSignCollection(**{
    "signs": {
        ZodiacSign.aries: {
            "sign": ZodiacSign.aries,
            "polarity": Polarity.yang,
            "modality": Modality.cardinal,
            "element": Element.fire,
            "rulership": Point.mars,
            "domicile": [Point.mars],
            "exaltation": [Point.sun],
            "detriment": [Point.venus],
            "fall": [Point.saturn],
            "decans": [Point.mars, Point.sun, Point.venus]
        },
        ZodiacSign.taurus: {
            "sign": ZodiacSign.taurus,
            "polarity": Polarity.yin,
            "modality": Modality.fixed,
            "element": Element.earth,
            "rulership": Point.venus,
            "domicile": [Point.venus],
            "exaltation": [Point.moon],
            "detriment": [Point.mars, Point.pluto],
            "fall": [Point.uranus],
            "decans": [Point.mercury, Point.moon, Point.saturn],
        },
        ZodiacSign.gemini: {
            "sign": ZodiacSign.gemini,
            "polarity": Polarity.yang,
            "modality": Modality.mutable,
            "element": Element.air,
            "rulership": Point.mercury,
            "domicile": [Point.mercury],
            "exaltation": [],
            "detriment": [Point.jupiter],
            "fall": [],
            "decans": [Point.jupiter, Point.mars, Point.sun],
        },
        ZodiacSign.cancer: {
            "sign": ZodiacSign.cancer,
            "polarity": Polarity.yin,
            "modality": Modality.cardinal,
            "element": Element.water,
            "rulership": Point.moon,
            "domicile": [Point.moon],
            "exaltation": [Point.jupiter],
            "detriment": [Point.saturn],
            "fall": [Point.mars],
            "decans": [Point.venus, Point.mercury, Point.moon],
        },
        ZodiacSign.leo: {
            "sign": ZodiacSign.leo,
            "polarity": Polarity.yang,
            "modality": Modality.fixed,
            "element": Element.fire,
            "rulership": Point.sun,
            "domicile": [Point.sun],
            "exaltation": [Point.pluto],
            "detriment": [Point.saturn, Point.uranus],
            "fall": [],
            "decans": [Point.saturn, Point.jupiter, Point.mars],
        },
        ZodiacSign.virgo: {
            "sign": ZodiacSign.virgo,
            "polarity": Polarity.yin,
            "modality": Modality.mutable,
            "element": Element.earth,
            "rulership": Point.mercury,
            "domicile": [Point.mercury],
            "exaltation": [],
            "detriment": [Point.jupiter, Point.neptune],
            "fall": [Point.venus],
            "decans": [Point.sun, Point.venus, Point.mercury],
        },
        ZodiacSign.libra: {
            "sign": ZodiacSign.libra,
            "polarity": Polarity.yang,
            "modality": Modality.cardinal,
            "element": Element.air,
            "rulership": Point.venus,
            "domicile": [Point.venus],
            "exaltation": [Point.saturn],
            "detriment": [Point.mars],
            "fall": [Point.sun],
            "decans": [Point.moon, Point.saturn, Point.jupiter],
        },
        ZodiacSign.scorpio: {
            "sign": ZodiacSign.scorpio,
            "polarity": Polarity.yin,
            "modality": Modality.fixed,
            "element": Element.water,
            "rulership": Point.mars,
            "domicile": [Point.mars, Point.pluto],
            "exaltation": [Point.uranus],
            "detriment": [Point.venus],
            "fall": [Point.moon],
            "decans": [Point.mars, Point.sun, Point.venus],
        },
        ZodiacSign.sagittarius: {
            "sign": ZodiacSign.sagittarius,
            "polarity": Polarity.yang,
            "modality": Modality.mutable,
            "element": Element.fire,
            "rulership": Point.jupiter,
            "domicile": [Point.jupiter],
            "exaltation": [],
            "detriment": [Point.mercury],
            "fall": [],
            "decans": [Point.mercury, Point.moon, Point.saturn],
        },
        ZodiacSign.capricorn: {
            "sign": ZodiacSign.capricorn,
            "polarity": Polarity.yin,
            "modality": Modality.cardinal,
            "element": Element.earth,
            "rulership": Point.saturn,
            "domicile": [Point.saturn],
            "exaltation": [Point.mars],
            "detriment": [Point.moon],
            "fall": [Point.jupiter, Point.neptune],
            "decans": [Point.jupiter, Point.mars, Point.sun],
        },
        ZodiacSign.aquarius: {
            "sign": ZodiacSign.aquarius,
            "polarity": Polarity.yang,
            "modality": Modality.fixed,
            "element": Element.air,
            "rulership": Point.saturn,
            "domicile": [Point.saturn, Point.uranus],
            "exaltation": [],
            "detriment": [Point.sun],
            "fall": [Point.pluto],
            "decans": [Point.venus, Point.mercury, Point.moon],
        },
        ZodiacSign.pisces: {
            "sign": ZodiacSign.pisces,
            "polarity": Polarity.yin,
            "modality": Modality.mutable,
            "element": Element.water,
            "rulership": Point.jupiter,
            "domicile": [Point.jupiter, Point.neptune],
            "exaltation": [Point.venus],
            "detriment": [Point.mercury],
            "fall": [],
            "decans": [Point.saturn, Point.jupiter, Point.mars],
        },
    }
})

# Exports the traditional order of zodiac signs.
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

# Associates each point with relevant information.
pointTraits = PointTraitsCollection(**{
    "points": {
        Point.moon: {
            "swe_id": swe.MOON,
            "name": Point.moon,
            "is_traditional": True,
        },
        Point.mercury: {
            "swe_id": swe.MERCURY,
            "name": Point.mercury,
            "is_traditional": True,
        },
        Point.venus: {
            "swe_id": swe.VENUS,
            "name": Point.venus,
            "is_traditional": True,
        },
        Point.sun: {
            "swe_id": swe.SUN,
            "name": Point.sun,
            "is_traditional": True,
        },
        Point.mars: {
            "swe_id": swe.MARS,
            "name": Point.mars,
            "is_traditional": True,
        },
        Point.jupiter: {
            "swe_id": swe.JUPITER,
            "name": Point.jupiter,
            "is_traditional": True,
        },
        Point.saturn: {
            "swe_id": swe.SATURN,
            "name": Point.saturn,
            "is_traditional": True,
        },
        Point.uranus: {
            "swe_id": swe.URANUS,
            "name": Point.uranus,
            "is_outer": True,
        },
        Point.neptune: {
            "swe_id": swe.NEPTUNE,
            "name": Point.neptune,
            "is_outer": True,
        },
        Point.pluto: {
            "swe_id": swe.PLUTO,
            "name": Point.pluto,
            "is_outer": True,
        },
    }
})
