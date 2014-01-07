
actions = {
# Syntax :
#   'action' : {
#       'min-ingredients': (integer) [optional]
#       'max-ingredients': (integer) #higher than min-ingredients# [optional]
#       'parameters-allowed': (list of parameters) [required]
#       'parameters-required': (integer) [optional]
#   }
    'melanger': {
        'min-ingredients': 2,
        'max-ingredients': 3,
        'parameters-allowed': ['duree', 'type_melanger'],
        'parameters-required': ['type_melanger', 'duree']
    },
    'cuire': {
        'min-ingredients':1,
        'parameters-allowed': ['duree','type_cuire', 'temperature']
    }
}

def enum_value_index(enum, v):
    try:
        return enum.index(v)
    except KeyError:
        pass
    return None

parameters = {

# Syntax :
#   'parameter' : {
#       'value-index':     <method>: returns None if invalid and the index if valid
#       'images':          <Array>: for each index of the 'value-index' a file path
#       'images-complete': <Array>: for each index of the 'value-index' True or False
#   }

    'type_cuire' : {
        'value-index': lambda v: enum_value_index( ['Four', 'Grill'], v),
        'images': [
            'four.png',
            'grill.png'
        ],
        'image-complete': [
            True,
            True
        ]
    },
    'type_melanger' : {
        'value-index': lambda v: enum_value_index( ['Fouet', 'Mixer'], v),
        'images': [
            'fouet.png',
            'mixer.png' 
        ],
        'image-complete': [
            True,
            True
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

def parameter_image(method, parameter, value):
    PREFIX = './images/'
    
    def query_index(par, val):
        return parameters[par]['value-index'](val)
    def query_image(par, ind):
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
        
    

parameter_dependencies = {
# Syntax :
#   'action' : (list of values OR parameters) OR (list of list of values OR parameters)
#   
#   Examples :
#       If an action has multiple sets of dependencies, use a list of lists, like so :
#   'cuire' : [
#       ['Four', 'temperature'],
#       ['Microonde', 'puissance']
#       ]
#
#       If an action has only one set of depedencies, use a simple list :
#   'melanger' : ['Mixer', 'duree']

    'cuire' : ['Four', 'temperature']
}
