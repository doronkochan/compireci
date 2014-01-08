
actions = {
# Syntax :
#   'action' : {
#       'min-ingredients':      <integer>: minimum amount of ingredient for the action [optional]
#       'max-ingredients':      <integer>: maximum amount of ingredient for the action #higher than min-ingredients# [optional]
#       'parameters-allowed':   <list of parameters>: which parameters are allowed for this action [required]
#       'parameters-required':  <integer>: which parameters are required for the action #all of these parameters have to be in parameters-allowed# [optional]
#   }
    'melanger': {
        'min-ingredients': 2,
        'max-ingredients': 10,
        'parameters-allowed': ['duree', 'type_melanger'],
        'parameters-required': ['type_melanger']
    },
    'cuire': {
        'min-ingredients': 1,
        'max-ingredients': 5,
        'parameters-allowed': ['duree', 'type_cuire', 'temperature', 'conteneur']
    },
    'repartir': {
        'min-ingredients': 1,
        'parameters-allowed': []
    },
    'petrir': {
        'min-ingredients': 1,
        'parameters-allowed':['type_petrir', 'duree']
    },
    'decouper': {
        'min-ingredients': 1,
        'max-ingredients': 1,
        'parameters-allowed':['type_decouper', 'morceaux']
    },
    'demouler' :{

    },
    'prechauffer': {
        'min-ingredients': 1,
        'max-ingredients': 1
    },
    'assaisonner': {
        'min-ingredients': 1,
        'max-ingredients': 5
    },
    'revenir': {

    }
}

parameters = {

# Syntax :
#   'parameter' : {
#       'value-index':     <method>: returns None if invalid and the index if valid [required]
#       'images':          <Array>: for each index of the 'value-index' a file path [optional]
#       'images-complete': <Array>: for each index of the 'value-index' True or False [optional]
#   }
    'conteneur' : {
        'value-index': lambda v: enum_value_index( ['Moule', 'Casserole', 'Plat'], v),
        'images': [
            None,
            None,
        ],
        'image-complete': [
            False,
            False
        ]
    },

    'type_cuire' : {
        'value-index': lambda v: enum_value_index( ['Four', 'Grill', 'BainMarie', 'Bouillir'], v),
        'images': [
            'four.png',
            'grill.png',
            None,
            None
        ],
        'image-complete': [
            True,
            True,
            False,
            False
        ]
    },
    'type_melanger' : {
        'value-index': lambda v: enum_value_index( ['Fouet', 'Mixer', 'Main'], v),
        'images': [
            'fouet.png',
            'mixer.png',
            None
        ],
        'image-complete': [
            True,
            True,
            False
        ]
    },
    'duree' : {
        'value-index': lambda v: 0,
        'images': [
            'duree.png'
        ],
        'image-complete': [
            False
        ]
    }
}

########
# DO NOT EDIT // TOOLS FOR SEMANTIC RULES ANALYSER
def enum_value_index(enum, v):
    try:
        return enum.index(v)
    except ValueError:
        pass
    return None

def parameter_image(method, parameter, value):
    PREFIX = './svgressource/images/'
    
    def query_index(par, val):
        return parameters[par]['value-index'](val)
    def query_image(par, ind):
        if parameters[par]['images'][ind] is None:
            return None
        
        return (
            PREFIX + parameters[par]['images'][ind],
            parameters[par]['image-complete'][ind]
        )
    
    try:
        index = query_index(parameter, value)
        return query_image(parameter, index);
    except KeyError:
        pass
    
    try:
        param = "%s_%s"%(parameter, method)
        index = query_index(param, value)
        return query_image(param, index);
    except KeyError:
        pass
    
    return None
########
    

parameter_dependencies = {
# Syntax :
#   'action' : (list of values OR parameters) OR (list of list of values OR parameters)
#   
#   Examples :
#       If an action has multiple sets of dependencies, use a list of lists, like so :
#   'cuire' : [
#           ['Four', 'temperature'],
#           ['Microonde', 'puissance']
#       ]
#
#       If an action has only one set of depedencies, use a simple list :
#   'melanger' : ['Mixer', 'duree']

    'cuire' : ['Four', 'temperature']
}
