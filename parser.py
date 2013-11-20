import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_instructions(p):
	''' instructions : instruction
		| instruction instructions '''
	p[0] = AST.InstructionsNode(p[1])

def p_instruction(p):
	''' instruction : VARIABLE '{' instructionbody '}' method '''
	p[0] = AST.InstructionNode([AST.TokenNode(p[1])]+p[3].children)

def p_instructionbody(p):
	''' instructionbody : TAB QUANTITY TEXT
		| TAB QUANTITY TEXT instructionbody '''
	p[0] = AST.TokenNode(p[2] + p[3])

def p_method(p):
	''' method : TEXT '(' parameters ')' '''
	p[0] = AST.InstructionNode([p[1]]+p[3].children)

def p_parameter_text(p):
	''' parameter : TEXT '=' TEXT '''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_parameter_qty(p):
	''' parameter : TEXT '=' QUANTITY '''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_parameters(p):
	''' parameters : parameter ',' parameters
		| parameter '''
	p[0] = AST.InstructionNode(p[1])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")

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