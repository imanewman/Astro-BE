import swisseph as swe

from src.definitions import ZodiacSign, Point

# Associates each zodiac sign with relevant information.
zodiacSignTraits = {
    ZodiacSign.aries: {},
    ZodiacSign.taurus: {},
    ZodiacSign.gemini: {},
    ZodiacSign.cancer: {},
    ZodiacSign.leo: {},
    ZodiacSign.virgo: {},
    ZodiacSign.libra: {},
    ZodiacSign.scorpio: {},
    ZodiacSign.sagittarius: {},
    ZodiacSign.capricorn: {},
    ZodiacSign.aquarius: {},
    ZodiacSign.pisces: {},
}

# Associates each point with relevant information.
pointTraits = {
    Point.moon: {
        id: swe.MOON,
    },
    Point.mercury: {
        id: swe.MERCURY,
    },
    Point.venus: {
        id: swe.VENUS,
    },
    Point.sun: {
        id: swe.SUN,
    },
    Point.mars: {
        id: swe.MARS,
    },
    Point.jupiter: {
        id: swe.JUPITER,
    },
    Point.saturn: {
        id: swe.SATURN,
    },
}
