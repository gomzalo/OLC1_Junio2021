''' 
José Puac
VACACIONES DE JUNIO 2020

INTERPRETER SAMPLE  
'''
import re
from TS.Excepcion import Excepcion

errores = []
reservadas = {
    'int'       : 'RINT',
    'float'     : 'RFLOAT',
    'string'    : 'RSTRING',
    'boolean'   : 'RBOOLEAN',
    'print'     : 'RPRINT',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
}

tokens  = [
    'PUNTOCOMA',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'MAS',
    'MENOS',
    'MENORQUE',
    'MAYORQUE',
    'IGUALIGUAL',
    'IGUAL',
    'AND',
    'OR',
    'NOT',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_MENORQUE      = r'<'
t_MAYORQUE      = r'>'
t_IGUALIGUAL    = r'=='
t_IGUAL         = r'='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex(reflags= re.IGNORECASE)

# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','UNOT'),
    ('left','MENORQUE','MAYORQUE', 'IGUALIGUAL'),
    ('left','MAS','MENOS'),
    ('right','UMENOS'),
    )

# Definición de la gramática

#Abstract
from Abstract.Instruccion import Instruccion
from Instrucciones.Imprimir import Imprimir
from Expresiones.Primitivos import Primitivos
from TS.Tipo import OperadorAritmetico, OperadorLogico, TIPO, OperadorRelacional
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Instrucciones.Declaracion import Declaracion
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.If import If

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : imprimir_instr finins
                        | declaracion_instr finins
                        | asignacion_instr finins
                        | if_instr'''
    t[0] = t[1]

def p_finins(t) :
    '''finins       : PUNTOCOMA
                    | '''
    t[0] = None

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sintáctico","Error Sintáctico." + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    'imprimir_instr     : RPRINT PARA expresion PARC'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////DECLARACION//////////////////////////////////////////////////

def p_declaracion(t) :
    'declaracion_instr     : tipo ID IGUAL expresion'
    t[0] = Declaracion(t[1], t[2], t.lineno(2), find_column(input, t.slice[2]), t[4])

#///////////////////////////////////////ASIGNACION//////////////////////////////////////////////////

def p_asignacion(t) :
    'asignacion_instr     : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////IF//////////////////////////////////////////////////

def p_if1(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE if_instr'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////TIPO//////////////////////////////////////////////////

def p_tipo(t) :
    '''tipo     : RINT
                | RFLOAT
                | RSTRING
                | RBOOLEAN '''
    if t[1] == 'int':
        t[0] = TIPO.ENTERO
    elif t[1] == 'float':
        t[0] = TIPO.DECIMAL
    elif t[1] == 'string':
        t[0] = TIPO.CADENA
    elif t[1] == 'boolean':
        t[0] = TIPO.BOOLEANO

#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion IGUALIGUAL expresion
            | expresion AND expresion
            | expresion OR expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
            | NOT expresion %prec UNOT 
    '''
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2],None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2],None, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

import ply.yacc as yacc
parser = yacc.yacc()

input = ''

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

#INTERFAZ

f = open("./entrada.txt", "r")
entrada = f.read()

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

instrucciones = parse(entrada.lower()) #ARBOL AST
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos()
ast.setTSglobal(TSGlobal)
for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    ast.getExcepciones().append(error)
    ast.updateConsola(error.toString())

for instruccion in ast.getInstrucciones():      # REALIZAR LAS ACCIONES
    value = instruccion.interpretar(ast,TSGlobal)
    if isinstance(value, Excepcion) :
        ast.getExcepciones().append(value)
        ast.updateConsola(value.toString())

print(ast.getConsola())