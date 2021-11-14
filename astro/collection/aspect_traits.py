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
        AspectType.bi_quintile: {
            "name": AspectType.bi_quintile,
            "degrees": 144,
        },

        AspectType.septile: {
            "name": AspectType.septile,
            "degrees": 360 / 7,
        },
        AspectType.bi_septile: {
            "name": AspectType.bi_septile,
            "degrees": 360 / 7 * 2,
        },
        AspectType.tri_septile: {
            "name": AspectType.tri_septile,
            "degrees": 360 / 7 * 3,
        },

        AspectType.octile: {
            "name": AspectType.octile,
            "degrees": 45,
        },
        AspectType.sesquiquadrate: {
            "name": AspectType.sesquiquadrate,
            "degrees": 135,
        },

        AspectType.novile: {
            "name": AspectType.novile,
            "degrees": 40,
        },
        AspectType.bi_novile: {
            "name": AspectType.bi_novile,
            "degrees": 80,
        },
        AspectType.quadri_novile: {
            "name": AspectType.quadri_novile,
            "degrees": 160,
        },

        AspectType.semi_sextile: {
            "name": AspectType.semi_sextile,
            "degrees": 30,
        },
        AspectType.quincunx: {
            "name": AspectType.quincunx,
            "degrees": 150,
        },
    }
})
"""
Associates each aspect with the degrees associated with it.
"""