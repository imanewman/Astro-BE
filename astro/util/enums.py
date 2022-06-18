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

    # Visible
    moon = "Moon"
    mercury = "Mercury"
    venus = "Venus"
    sun = "Sun"
    mars = "Mars"
    jupiter = "Jupiter"
    saturn = "Saturn"

    # Outer
    uranus = "Uranus"
    neptune = "Neptune"
    pluto = "Pluto"

    # Centaur
    chiron = "Chiron"
    pholus = "Pholus"
    chariklo = "Chariklo"

    # Common Asteroids
    ceres = "Ceres"
    pallas = "Pallas"
    juno = "Juno"
    vesta = "Vesta"

    # Uncommon Asteroids
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

    # Calculated Points
    ascendant = "Ascendant"
    midheaven = "Midheaven"
    descendant = "Descendant"
    inner_heaven = "Inner Heaven"
    vertex = "Vertex"

    # Nodes
    north_mode = "True North Node"
    south_node = "True South Node"

    # Egyptian/Arabic Lots
    lot_of_fortune = "Lot of Fortune"  # Moon
    lot_of_spirit = "Lot of Spirit"  # Sun
    lot_of_necessity = "Lot of Necessity"  # Mercury
    lot_of_eros= "Lot of Eros"  # Venus
    lot_of_courage = "Lot of Courage"  # Mars
    lot_of_victory = "Lot of Victory"  # Jupiter
    lot_of_nemesis = "Lot of Nemesis"  # Saturn


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
    conjunction = "Conjunction"  # 1
    opposition = "Opposition"  # 1/2
    trine = "Trine"  # 1/3
    square = "Square"  # 1/4
    sextile = "Sextile"  # 1/6

    quintile = "Quintile"  # 1/5
    bi_quintile = "Bi-Quintile"  # 2/5

    septile = "Septile"  # 1/7
    bi_septile = "Bi-Septile"  # 2/7
    tri_septile = "Tri-Septile"  # 3/7

    octile = "Octile"  # 1/8
    sesquiquadrate = "Sesquiquadrate"  # 3/8

    novile = "Novile"  # 1/9
    bi_novile = "Bi-Novile"  # 2/9
    quadri_novile = "Quadri-Novile"  # 4/9

    semi_sextile = "Semi-Sextile"  # 1/12
    quincunx = "Quincunx"  # 5/12

    parallel = "Parallel"  # 1
    contraparallel = "Contraparallel"  # -1

    aversion = "Aversion"  # 1/12, 5/12, 7/12, 11/12


class SectPlacement(str, Enum):
    """
    Enumerates the possible sect based statuses of a planet.
    """
    sect_light = "Sect Light"
    benefic_by_sect = "Benefic By Sect"
    benefic_contrary_sect = "Benefic Contrary To Sect"
    malefic_by_sect = "Malefic By Sect"
    malefic_contrary_sect = "Malefic Contrary To Sect"


class SunCondition(str, Enum):
    """
    Enumerates the possible sun conditions of a planet conjunct the Sun.
    """
    under_the_beams = "Under The Beams"
    combust = "Combust"
    cazimi = "Cazimi"


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


class AspectMovementType(str, Enum):
    """
    Enumerates all the aspect movement types.
    """
    applying = "Applying"
    mutually_applying = "Applying (M)"
    separating = "Separating"
    mutually_separating = "Separating (M)"


applying_aspects = [AspectMovementType.applying, AspectMovementType.mutually_applying]


class AspectSortType(str, Enum):
    """
    Enumerates all the aspect sort types.
    """
    point_order = "Point Order"
    smallest_orb = "Smallest Orb"
    no_sort = "No Sort"


class RulershipType(str, Enum):
    """
    Enumerates all the possible sign rulership schemes.
    """
    traditional = "Traditional"
    modern = "Modern"
    asteroids = "Asteroids"


class TransitType(str, Enum):
    """
    Enumerates all the possible transit calculation types.
    """
    transit_to_chart = "Transit To Chart"
    transit_to_transit = "Transit To Transit"


class TransitGroupType(str, Enum):
    """
    Enumerates all the possible transit group types.
    """
    all = "All"
    by_relationship = "By Relationship"
    by_natal_point = "By Natal Point"
    by_transit_point = "By Transit Point"
    by_day = "By Day"

