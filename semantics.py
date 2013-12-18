import AST
from lex import time_units
from AST import addToClass

#Tools
semantically_correct = True

#CONSTANTS
INGREDIENTS_NB_MAX = 10

actions = {
    'melanger': {
        'min-ingredients': 2,
        'max-ingredients': 3,
        'parameters-allowed': ['duree', 'type_melanger'],
        'parameters-required': ['type_melanger', 'duree']
    },
    'cuire': {
        'parameters-allowed': ['duree','type_cuire']
    }
}

parameters = {
    #'duree' : {
    #    'format': r'\d(\.?\d*)+(' + "|".join(time_units) + ')?(?!\w)'
    #},
    'type_cuire' : {
        #'name': 'type',
        'values-allowed': ['Four', 'Grill']
    },
    'type_melanger' : {
        #'name': 'type',
        'values-allowed': ['Fouet', 'Mixer']
    }
}

@addToClass(AST.InstructionsNode)
def verify(self):
    for instruction in self.children:
        # Result-ingredient recursion prevention (an ingredient has the same name as the resultant variable name)
        #for c in instruction.children:
        #    if isinstance(c, AST.TokenNode): # The ingredient is a variable
        #        if 
        instruction.verify()

@addToClass(AST.InstructionNode)
def verify(self):
    result_variable_name = self.children[0].tok

    ingredients_node = self.children[1]
    ingredient_list = ingredients_node.children
    method_node = self.children[2]

    ### Instructionbody
    #1 Number of ingredients according to method
    nb_ingredients = len(ingredient_list) # second child is the ingredients node
    method_name = str(method_node.children[0].tok) # 3rd child->1st child = method->methodname

    min_nb_ingredients = 0
    max_nb_ingredients = INGREDIENTS_NB_MAX

    try:
        min_nb_ingredients = actions[method_name]['min-ingredients']
    except KeyError:
        pass

    try:
        max_nb_ingredients = actions[method_name]['max-ingredients']
    except KeyError:
        pass
    
    if (nb_ingredients < min_nb_ingredients):
        sem_error(result_variable_name + ": not enough ingredients!")

    if (nb_ingredients > max_nb_ingredients):
        sem_error(result_variable_name + ": too many ingredients!")

    #4 Result-ingredient recursion prevention (an ingredient has the same name as the resultant variable name)
    for c in ingredient_list:
        if isinstance(c, AST.TokenNode): # The ingredient is a variable
            if (c.tok == result_variable_name):
                sem_error(result_variable_name + ': recursion detected!')

    ### Parameters
    method_parameters_list = method_node.children[1].children
    
    parameter_gathered_list = []
    #6 Parameters allowed check

    for c in method_parameters_list:
        parameters_allowed = actions[method_name]['parameters-allowed']
        parameter_name = c.children[0].tok

        #10 Repetition check
        if (parameter_name in parameter_gathered_list):
            sem_error(method_name + '[' + result_variable_name + ']' + ' : ' + \
                parameter_name + ' is repeated!')

        #Gather all the parameters to check if the required parameters are all present (#7, done later)
        parameter_gathered_list.append(parameter_name)


        #Check if the parameter is allowed
        if (
            parameter_name not in parameters_allowed and
            (parameter_name + '_' + method_name) not in parameters_allowed
            ):
            sem_error(method_name + '[' + result_variable_name + ']' + ' : ' + parameter_name + ' is not in the allowed parameters list')

    #7 Parameters required check
    parameters_required = actions[method_name]['parameters-required']

    parameters_missing = []
    for p in parameters_required:
        if (
            p not in parameter_gathered_list and
            p.split('_')[0] not in parameter_gathered_list
            ):
            parameters_missing.append(p)

    if (len(parameters_missing) > 0):
        if (len(parameters_missing)==1):
            sem_error(method_name + '[' + result_variable_name + ']' + ' : ' + 'required parameter \
'+ " and ".join(parameters_missing) + ' is missing!')
        else:
            sem_error(method_name + '[' + result_variable_name + ']' + ' : ' + 'required parameters \
'+ " and ".join(parameters_missing) + ' are missing!')

    #11 Parameter value restrictions
    for c in method_parameters_list:
        p = c.children[0].tok
        v = c.children[1].tok
        param_name = ''
        if (p in parameters):
            param_name = p
        elif ((p+'_'+method_name) in parameters):
            param_name = p+'_'+method_name
        else: continue

        if (v not in parameters[param_name]['values-allowed']
            #Regex with format field in parameters ?
            ):
            sem_error(method_name + '[' + result_variable_name + ']' + ' : '+'parameter ' + p + ' can\'t have value ' + v)

def sem_error(message):
    print(message)
    global semantically_correct
    semantically_correct = False

def semantic(prog): # Useful ??
    ast = parse(prog)
    ast.verify()

if __name__ == '__main__':
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()

    ast = parse(prog)

    ast.verify()
    if (semantically_correct is True):
        print('Semantics OK!')
        #SVG GEN now?
    else:
        print('Semantics Error!')