from enum import Enum

from pydantic import BaseModel


# Enumerates all of the zodiac signs.
class ZodiacSign(str, Enum):
    aries = "Aries"
    taurus = "Taurus"
    gemini = "Gemini"
    cancer = "Cancer"
    leo = "Leo"
    virgo = "Virgo"
    libra = "Libra"
    scorpio = "Scorpio"
    sagittarius = "Sagittarius"
    capricorn = "Capricorn"
    aquarius = "Aquarius"
    pisces = "Pisces"


# Enumerates all of the available points and planetary bodies.
class Point(str, Enum):
    moon = "Moon"
    mercury = "Mercury"
    venus = "Venus"
    sun = "Sun"
    mars = "Mars"
    jupiter = "Jupiter"
    saturn = "Saturn"


# Defines any planetary body's position relative to Earth.
class PointInTime(BaseModel):
    # The name of the point.
    name: Point
    # The degrees (out of 360) that this point is located at.
    degrees_from_aries: float
    # The zodiac sign this point is located within.
    sign: ZodiacSign
    # The degrees (out of 30) within a sign that this point is located at.
    degrees_in_sign: int
    # The minutes (out of 60) within a degree that this point is located at.
    minutes_in_sign: int
