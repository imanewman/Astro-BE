from astro.schema import LotTraitsCollection
from astro.util import Point

lot_traits = LotTraitsCollection(lots={
    Point.lot_of_fortune: {
        "id": Point.lot_of_fortune,
        "name": "Lot of Fortune",
        "add_point": Point.moon,
        "sub_point": Point.sun,
        "reverse_at_night": True,
    },
    Point.lot_of_spirit: {
        "id": Point.lot_of_spirit,
        "name": "Lot of Spirit",
        "add_point": Point.sun,
        "sub_point": Point.moon,
        "reverse_at_night": True,
    },
    Point.lot_of_necessity: {
        "id": Point.lot_of_necessity,
        "name": "Mercury, Lot of Necessity",
        "add_point": Point.lot_of_fortune,
        "sub_point": Point.mercury,
        "reverse_at_night": True,
    },
    Point.lot_of_eros: {
        "id": Point.lot_of_eros,
        "name": "Venus, Lot of Eros",
        "add_point": Point.venus,
        "sub_point": Point.lot_of_spirit,
        "reverse_at_night": True,
    },
    Point.lot_of_courage: {
        "id": Point.lot_of_courage,
        "name": "Mars, Lot of Courage",
        "add_point": Point.lot_of_fortune,
        "sub_point": Point.mars,
        "reverse_at_night": True,
    },
    Point.lot_of_victory: {
        "id": Point.lot_of_victory,
        "name": "Jupiter, Lot of Victory",
        "add_point": Point.jupiter,
        "sub_point": Point.lot_of_spirit,
        "reverse_at_night": True,
    },
    Point.lot_of_nemesis: {
        "id": Point.lot_of_nemesis,
        "name": "Saturn, Lot of Nemesis",
        "add_point": Point.lot_of_fortune,
        "sub_point": Point.saturn,
        "reverse_at_night": True,
    },
})
"""
Defines the equations for the preset arabic lots.

- Lot calculates and usage by Rob Hand: https://www.astro.com/astrology/in_fortune_e.htm 
"""
