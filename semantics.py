import AST
from lex import time_units
from AST import addToClass

# CONSTANTS

INGREDIENTS_NB_MAX = 10

actions = {
    'melanger': {
        'min-ingredients': 2,
        'max-ingredients': 3,
        'parameters-allowed': ['duree', 'type_melanger'],
        'parameters-required': ['type']
    },
    'cuire': {
        'parameters-allowed': ['duree','type_cuire']
    }
}

parameters = {
    'duree' : {
        'format': r'\d(\.?\d*)+(' + "|".join(time_units) + ')?(?!\w)'
    },
    'type_cuire' : {
        'name': 'type',
        'values': ['Four', 'Grill']
    },
    'type_melanger' : {
        'name': 'type',
        'values': ['Fouet', 'Mixer']
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

    # Number of ingredients according to method
    nb_ingredients = len(self.children[1].children)
    method_name = str(self.children[2].children[0].tok)

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
        print(self.children[0].tok + ": not enough ingredients!")

    if (nb_ingredients > max_nb_ingredients):
        print(self.children[0].tok + ": too many ingredients!")

    # Result-ingredient recursion prevention (an ingredient has the same name as the resultant variable name)
    for c in self.children[1].children:
        if isinstance(c, AST.TokenNode): # The ingredient is a variable
            if (c.tok == self.children[0].tok):
                print (self.children[0].tok + ': recursion detected!')

    # Carry on
    for c in self.children:
        c.verify()



@addToClass(AST.InstructionBodyNode)
def verify(self):
    # Carry on
    for c in self.children:
        c.verify()


@addToClass(AST.TokenNode)
def verify(self):
    return self.tok

@addToClass(AST.MethodArgumentNode)
def verify(self):
    pass

@addToClass(AST.QuantityNode)
def verify(self):
    # Carry on
    for c in self.children:
        c.verify()

@addToClass(AST.IngredientNode)
def verify(self):
    pass

@addToClass(AST.MethodNode)
def verify(self):
    for param in self.children[1].children:
        # Check allowed and required parameters
        param_name = param.children[0].tok
        # IN CONSTRUCTION

@addToClass(AST.MethodParametersNode)
def verify(self):
    pass


if __name__ == '__main__':
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()

    ast = parse(prog)

    ast.verify()