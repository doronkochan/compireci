#!/usr/bin/env python

import sys
import getopt

from parts.lex import analyse_lex
from parts.parser import analyse_syn
from parts.semantics import analyse_sem
from parts.generator import generate_svg

def usage():
    print( " usage: %s [options] [params]" % sys.argv[0] )
    print( "")
    print( "")
    print( "  options: " )
    print( "   -h, --help Show this help" )
    print( "   -t, --tree-pdf  create AST pdf" )
    print( "   -o, --tree-out  displays the AST on the std out" )
    print("")
    print( "  params: " )
    print( "   -m VALUE, --mode=VALUE       Execution mode (default: gen)" )
    print( "        valid VALUES: lex   executes the analyse lexicale (level 1)" )
    print( "                      syn   executes the analyse syntaxic (level 2)" )
    print( "                      sem   executes the analyse semantic (level 3)" )
    print( "                      gen   generates the svg image       (level 4)" )
    print( "          each time the levels below are executed as well" )
    print( "")
    print( "   -r VALUE, --recipe=VALUE     recipi file name ")
    print("")
    print(" (c) 2014 by Danick Fort and Marco Aeberli")
    print("")
    print("")

def get_argv_params():
    try:
        opts = getopt.getopt(
            sys.argv[1:],
            "htom:r:",
            ["help","tree-pdf","tree-out","mode=","recipe="] )[0]
    except getopt.GetoptError:
        usage()
        print("Wrong options or params.")
        exit(2)
        
    astPDF = False
    astOUT = False
    mode = 'gen'
    recipe = None
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit()
        elif opt in ("-t", "--tree-pdf"):
            astPDF = True
        elif opt in ("-o", "--tree-out"):
            astOUT = True
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-r", "--recipe"):
            recipe = arg
    
    if mode not in ['lex', 'syn', 'sem', 'gen']:
        usage()
        print("Not a valid mode")
        exit(2)
    
    if recipe is None:
        usage()
        print("Recipe parameter required.")
        exit(2)
    
    return (mode, recipe, astPDF, astOUT)

if __name__ == "__main__":
    (mode, recipe, astPDF, astOUT) = get_argv_params()
    
    if mode == 'lex':
        analyse_lex(recipe)
    elif mode == 'syn':
        analyse_syn(recipe, astPDF, astOUT)
    elif mode == 'sem':
        analyse_sem(recipe)
    elif mode == 'gen':
        if analyse_sem(recipe):
            generate_svg(recipe)
