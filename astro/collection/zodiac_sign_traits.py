from astro.schema import ZodiacSignCollection
from astro.collection.zodiac_signs import *

zodiac_sign_traits = ZodiacSignCollection(
    signs={
        ZodiacSign.aries: zodiac_sign_aries,
        ZodiacSign.taurus: zodiac_sign_taurus,
        ZodiacSign.gemini: zodiac_sign_gemini,
        ZodiacSign.cancer: zodiac_sign_cancer,
        ZodiacSign.leo: zodiac_sign_leo,
        ZodiacSign.virgo: zodiac_sign_virgo,
        ZodiacSign.libra: zodiac_sign_libra,
        ZodiacSign.scorpio: zodiac_sign_scorpio,
        ZodiacSign.sagittarius: zodiac_sign_sagittarius,
        ZodiacSign.capricorn: zodiac_sign_aries,
        ZodiacSign.aquarius: zodiac_sign_aquarius,
        ZodiacSign.pisces: zodiac_sign_pisces
    }
)
"""
Associates each zodiac sign with relevant information.

- Reference for essential dignities: 
    https://theastrologypodcast.com/wp-content/uploads/2018/05/essential-dignities-table-large.jpg
"""
