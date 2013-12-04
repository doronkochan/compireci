import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_instructions(p):
    ''' instructions : instruction
        | instructions instruction '''
    if (len(p) > 2):
        p[0] = AST.InstructionsNode(p[1].children + [p[2]])
    else:
        p[0] = AST.InstructionNode(p[1])

def p_instruction(p):
    ''' instruction : VARIABLE '{' instructionbody '}' method '''
    p[0] = AST.InstructionNode([AST.TokenNode(p[1])]+[p[3]]+[p[5]])

def p_instructionbody(p):
    ''' instructionbody : ingredient
        | ingredient instructionbody '''
    if (len(p) > 2):
        p[0] = AST.InstructionBodyNode([p[1]] + p[2].children)
    else:
        p[0] = AST.InstructionBodyNode(p[1])

def p_instructionbody_variable(p):
    ''' instructionbody : TAB VARIABLE
        | TAB VARIABLE instructionbody '''
    if (len(p) > 3):
        p[0] = AST.InstructionBodyNode([AST.TokenNode(p[2])] + p[3].children)
    else:
        p[0] = AST.InstructionBodyNode(AST.TokenNode(p[2]))

def p_ingredient(p):
    ''' ingredient : TAB QUANTITY TEXT '''
    p[0] = AST.IngredientNode([AST.QuantityNode(AST.TokenNode(p[2]))] + [AST.TokenNode(p[3])])

def p_method(p):
    ''' method : TEXT '(' parameters ')' '''
    p[0] = AST.MethodNode([AST.TokenNode(p[1]),p[3]])

def p_parameter_text(p):
    ''' parameter : TEXT '=' TEXT '''
    p[0] = AST.MethodArgumentNode([AST.TokenNode(p[1]),AST.TokenNode(p[3])])

def p_parameter_qty(p):
    ''' parameter : TEXT '=' QUANTITY '''
    p[0] = AST.MethodArgumentNode([AST.TokenNode(p[1]),AST.TokenNode(p[3])])

def p_parameters(p):
    ''' parameters : parameter ',' parameters
        | parameter
        |   '''
    if (len(p) > 3):
        p[0] = AST.MethodParametersNode([p[1]]+ p[3].children)
    elif (len(p) > 1):
        p[0] = AST.MethodParametersNode(p[1])
    else:
        p[0] = AST.MethodParametersNode()

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Syntax error: unexpected end of file!")

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog,debug=1)
    if result:
        print (result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")