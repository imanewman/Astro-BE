from astro.schema import ZodiacSignTraits
from astro.util import ZodiacSign, Polarity, Modality, Element, Point

zodiac_sign_pisces = ZodiacSignTraits(**{
    "sign": ZodiacSign.pisces,
    "polarity": Polarity.yin,
    "modality": Modality.mutable,
    "element": Element.water,
    "domicile_traditional": Point.jupiter,
    "domicile_modern": Point.jupiter,
    "domicile_asteroid": [],
    "exaltation": Point.venus,
    "triplicity": [Point.venus, Point.mars, Point.moon],
    "bounds": [
        {"ruler": Point.venus, "to_degree": 12},
        {"ruler": Point.jupiter, "to_degree": 16},
        {"ruler": Point.mercury, "to_degree": 19},
        {"ruler": Point.mars, "to_degree": 28},
        {"ruler": Point.saturn, "to_degree": 30},
    ],
    "decans": [
        {"ruler": Point.saturn, "to_degree": 10},
        {"ruler": Point.jupiter, "to_degree": 20},
        {"ruler": Point.mars, "to_degree": 30},
    ],
    "twelfth_parts": [
        {"sign": ZodiacSign.pisces, "to_degree": 2.5},
        {"sign": ZodiacSign.aries, "to_degree": 5},
        {"sign": ZodiacSign.taurus, "to_degree": 7.5},
        {"sign": ZodiacSign.gemini, "to_degree": 10},
        {"sign": ZodiacSign.cancer, "to_degree": 12.5},
        {"sign": ZodiacSign.leo, "to_degree": 15},
        {"sign": ZodiacSign.virgo, "to_degree": 17.5},
        {"sign": ZodiacSign.libra, "to_degree": 20},
        {"sign": ZodiacSign.scorpio, "to_degree": 22.5},
        {"sign": ZodiacSign.sagittarius, "to_degree": 25},
        {"sign": ZodiacSign.capricorn, "to_degree": 27.5},
        {"sign": ZodiacSign.aquarius, "to_degree": 30},
    ],
    "degrees": [
        {"sign": ZodiacSign.pisces, "sabian_symbol": ""},
        {"sign": ZodiacSign.aries, "sabian_symbol": ""},
        {"sign": ZodiacSign.taurus, "sabian_symbol": ""},
        {"sign": ZodiacSign.gemini, "sabian_symbol": ""},
        {"sign": ZodiacSign.cancer, "sabian_symbol": ""},
        {"sign": ZodiacSign.leo, "sabian_symbol": ""},
        {"sign": ZodiacSign.virgo, "sabian_symbol": ""},
        {"sign": ZodiacSign.libra, "sabian_symbol": ""},
        {"sign": ZodiacSign.scorpio, "sabian_symbol": ""},
        {"sign": ZodiacSign.sagittarius, "sabian_symbol": ""},
        {"sign": ZodiacSign.capricorn, "sabian_symbol": ""},
        {"sign": ZodiacSign.aquarius, "sabian_symbol": ""},
        {"sign": ZodiacSign.pisces, "sabian_symbol": ""},
        {"sign": ZodiacSign.aries, "sabian_symbol": ""},
        {"sign": ZodiacSign.taurus, "sabian_symbol": ""},
        {"sign": ZodiacSign.gemini, "sabian_symbol": ""},
        {"sign": ZodiacSign.cancer, "sabian_symbol": ""},
        {"sign": ZodiacSign.leo, "sabian_symbol": ""},
        {"sign": ZodiacSign.virgo, "sabian_symbol": ""},
        {"sign": ZodiacSign.libra, "sabian_symbol": ""},
        {"sign": ZodiacSign.scorpio, "sabian_symbol": ""},
        {"sign": ZodiacSign.sagittarius, "sabian_symbol": ""},
        {"sign": ZodiacSign.capricorn, "sabian_symbol": ""},
        {"sign": ZodiacSign.aquarius, "sabian_symbol": ""},
        {"sign": ZodiacSign.pisces, "sabian_symbol": ""},
        {"sign": ZodiacSign.aries, "sabian_symbol": ""},
        {"sign": ZodiacSign.taurus, "sabian_symbol": ""},
        {"sign": ZodiacSign.gemini, "sabian_symbol": ""},
        {"sign": ZodiacSign.cancer, "sabian_symbol": ""},
        {"sign": ZodiacSign.leo, "sabian_symbol": ""},
    ],
    "detriment": Point.mercury,
    "fall": None,
})
