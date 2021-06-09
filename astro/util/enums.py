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


class Point(str, Enum):
    """
    Enumerates all of the available points and planetary bodies.
    """
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
    psyche = "Psyche"
    charklo = "Charklo"
    eros = "Eros"
    eris = "Eris"

    north_mode = "North Node"
    south_node = "South Node"


class PointCategory(str, Enum):
    """
    Enumerates the different types of points.
    """

    visible = "Visible Planet"
    outer = "Outer Planet"
    point = "Calculated Point"


class AspectType(str, Enum):
    """
    Enumerates the different types of aspects between points.
    """
    conjunction = "Conjunction"
    opposition = "Opposition"
    square = "Square"
    trine = "Trine"
    sextile = "Sextile"

    quintile = "Quintile"
    septile = "Septile"
    octile = "Octile"
    novile = "Novile"
    semi_sextile = "Semi-Sextile"
    quincunx = "Quincunx"
    sesquiquadrate = "Sesquiquadrate"
    bi_quintile = "Bi-Quintile"

    parallel = "Parallel"
    contraparallel = "Contraparallel"

    aversion = "Aversion"


class SectPlacement(str, Enum):
    """
    Enumerates the possible sect based statuses of a planet.
    """
    sect_light = "Sect Light"
    benefic_by_sect = "Benefic By Sect"
    benefic_contrary_sect = "Benefic Contrary To Sect"
    malefic_by_sect = "Malefic By Sect"
    malefic_contrary_sect = "Malefic Contrary To Sect"


class PhaseType(str, Enum):
    """
    The phase between two points, dividing the 360 degree arc into eighths
    """
    new = "New"
    crescent = "Crescent"
    first_quarter = "First Quarter"
    gibbous = "Gibbous"
    full = "Full"
    disseminating = "Disseminating"
    last_quarter = "Last Quarter"
    balsamic = "Balsamic"

