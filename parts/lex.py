import ply.lex as lex
from ply.lex import TOKEN

errorOccured = False

reserved_words = (
	#actions?
)

tokens = (
	'VARIABLE',
	'QUANTITY',
	'TEXT',
	'TAB'
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '()=,{}\t'

time_units = ['jour','h','m','s']
units = ['kg','g','mg','l','dl','cl','ml','pincee','cas','cac','peu'] + time_units

qty_pattern = r'\d(\.?\d*)+(' + "|".join(units) + ')?(?!\w)'

t_ignore = ' '

def t_TAB(t):
	r'\t'
	return t

def t_VARIABLE(t):
	r'_\w+'
	return t

@TOKEN(qty_pattern)
def t_QUANTITY(t):
	return t

def t_TEXT(t):
	r'[A-Za-z]\w*'
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	errorOccured = True
	t.lexer.skip(1)

lex.lex()

def analyse_lex(filename):
    prog = open(filename).read()
    
    lex.input(prog)
    
    while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
    
    return not errorOccured

if __name__ == "__main__":
	import sys
	analyse_lex(sys.argv[1])
