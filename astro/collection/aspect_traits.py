from astro.schema import AspectTraitsCollection
from astro.util import AspectType

aspectTraits = AspectTraitsCollection(**{
    "aspects": {
        AspectType.conjunction: {
            "name": AspectType.conjunction,
            "degrees": 0,
        },
        AspectType.opposition: {
            "name": AspectType.opposition,
            "degrees": 180,
        },
        AspectType.square: {
            "name": AspectType.square,
            "degrees": 90,
        },
        AspectType.trine: {
            "name": AspectType.trine,
            "degrees": 120,
        },
        AspectType.sextile: {
            "name": AspectType.sextile,
            "degrees": 60,
        },
        AspectType.quintile: {
            "name": AspectType.quintile,
            "degrees": 72,
        },
        AspectType.septile: {
            "name": AspectType.septile,
            "degrees": 51,
        },
        AspectType.octile: {
            "name": AspectType.octile,
            "degrees": 45,
        },
        AspectType.novile: {
            "name": AspectType.novile,
            "degrees": 40,
        },
        AspectType.semi_sextile: {
            "name": AspectType.semi_sextile,
            "degrees": 30,
        },
        AspectType.quincunx: {
            "name": AspectType.quincunx,
            "degrees": 150,
        },
        AspectType.sesquiquadrate: {
            "name": AspectType.sesquiquadrate,
            "degrees": 135,
        },
        AspectType.bi_quintile: {
            "name": AspectType.bi_quintile,
            "degrees": 144,
        },
    }
})
"""
Associates each aspect with the degrees associated with it.
"""