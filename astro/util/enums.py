from enum import Enum


class EventType(str, Enum):
    """
    Enumerates all of the event types.
    """

    natal = "Natal"
    transit = "Transit"
    event = "Event"
    horary = "Horary"
    election = "Election"


class AspectMovementType(str, Enum):
    """
    Enumerates all of the aspect movement types.
    """

    applying = "Applying"
    mutually_applying = "Mutually Applying"
    separating = "Separating"
    mutually_separating = "Mutually Separating"


class AspectSortType(str, Enum):
    """
    Enumerates all of the aspect sort types.
    """

    point_order = "Point Order"
    smallest_orb = "Smallest Orb"


class HouseSystem(str, Enum):
    """
    Enumerates all of the house systems.
    """

    whole_sign = "Whole Sign"  # W
    placidus = "Placidus"  # P
    equal = "Equal"  # E
    porphyry = "Porphyry"  # O
    regiomontanus = "Regiomontanus"  # R
    campanus = "Campanus"  # C


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
    charklo = "Charklo"

    ceres = "Ceres"
    pallas = "Pallas"
    juno = "Juno"
    vesta = "Vesta"

    psyche = "Psyche"
    eros = "Eros"
    lilith = "Lilith"
    toro = "Toro"
    sappho = "Sappho"
    amor = "Amor"
    pandora = "Pandora"
    icarus = "Icarus"
    diana = "Diana"
    hidalgo = "Hidalgo"
    urania = "Urania"
    eris = "Eris"

    ascendant = "Ascendant"
    midheaven = "Midheaven"
    descendant = "Descendant"
    inner_heaven = "Inner Heaven"
    vertex = "Vertex"

    north_mode = "North Node"
    south_node = "South Node"


class PointAssociation(str, Enum):
    """
    Enumerates the different associations of points to one's life.
    """

    personal = "Personal Planet"
    social = "Social Planet"
    transpersonal = "Transpersonal Planet"
    transformational = "Transformational Planet"


class PointCategory(str, Enum):
    """
    Enumerates the different types of points.
    """

    visible = "Visible Planet"
    outer = "Outer Planet"
    asteroid = "Asteroid"
    TNO = "Trans Neptunian Object"
    centaur = "Centaur"
    transplutonian = "Transplutonian"
    point = "Point"


class AspectType(str, Enum):
    """
    Enumerates the different types of aspects between points.
    """

    conjunction = "Conjunction"
    opposition = "Opposition"
    trine = "Trine"
    square = "Square"
    sextile = "Sextile"

    quintile = "Quintile"
    septile = "Septile"
    octile = "Octile (Semi-Square)"
    novile = "Novile"
    semi_sextile = "Semi-Sextile"
    quincunx = "Quincunx (Inconjunct)"
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

