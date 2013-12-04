from lex import time_units

actions = {
    'melanger': {
        'min-ingredients': 2,
        'parameters-allowed': ['duree', 'type_melanger'],
        'parameters-required': ['type']
    },
    'cuire': {
        'min-ingredients': 0,
        'parameters-allowed': ['duree','type_cuire']
    }
}

parameters = {
    'duree' : {
        'format': r'\d(\.?\d*)+(' + "|".join(time_units) + ')?(?!\w)'
    },
    'type_cuire' : {
        'name': 'type',
        'values': 'Four', 'Grill' 
    }
    'type_melanger' : {
        'name': 'type',
        'values': 'Fouet', 'Mixer' 
    }
}