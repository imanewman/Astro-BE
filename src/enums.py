from enum import Enum


# Enumerates all of the elements
class Polarity(str, Enum):
    yang = "Yang"
    yin = "Yin"


# Enumerates all of the elements
class Modality(str, Enum):
    cardinal = "Cardinal"
    fixed = "Fixed"
    mutable = "Mutable"


# Enumerates all of the elements
class Element(str, Enum):
    fire = "Fire"
    air = "Air"
    water = "Water"
    earth = "Earth"


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
    uranus = "Uranus"
    neptune = "Neptune"
    pluto = "Pluto"
