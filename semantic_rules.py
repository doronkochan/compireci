
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

parameters = {

# Syntax :
#   'parameter' : {
#       'values-allowed': (list of values)
#   }

    'type_cuire' : {
        'values-allowed': ['Four', 'Grill']
    },
    'type_melanger' : {
        'values-allowed': ['Fouet', 'Mixer']
    }
}

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