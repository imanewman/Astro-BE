from enum import Enum


class Polarity(str, Enum):
    """
    Enumerates all of the polarities.
    """
    yang = "Yang"
    yin = "Yin"


class Modality(str, Enum):
    """
    Enumerates all of the modalities.
    """
    cardinal = "Cardinal"
    fixed = "Fixed"
    mutable = "Mutable"


class Element(str, Enum):
    """
    Enumerates all of the elements.
    """
    fire = "Fire"
    air = "Air"
    water = "Water"
    earth = "Earth"


class ZodiacSign(str, Enum):
    """
    Enumerates all of the zodiac signs.
    """

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
    ascendant = "Ascendant"
    midheaven = "Midheaven"

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

    chiron = "Chiron"
    pholus = "Pholus"
    ceres = "Ceres"
    pallas = "Pallas"
    juno = "Juno"
    vesta = "Vesta"


class PointCategory(str, Enum):
    visible = "Visible Planet"
    outer = "Outer Planet"
