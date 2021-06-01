'''

Gramatica PLY
Vacaciones Junio 2021

'''

tokens = (
    'ROPERAR',
    'PARA',
    'PARC',
    'CORA',
    'CORC',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'DECIMAL',
    'ENTERO',
    'PTCOMA'
)

#tokens
t_ROPERAR   = r'operar'
t_PARA      = r'\('
t_PARC      = r'\)'
t_CORA      = r'\['
t_CORC      = r'\]'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIV       = r'/'
t_PTCOMA    = r';'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("El valor es demasiado grande '%d'" % t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large '%d'" % t.value)
        t.value = 0
    return t

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno = t.value.count("\n")

def t_error(t): #LEXICOS
    print('caracter no reconocido: ' + str(t.value[0]))
    # almacenamiento de errores lexicos
    t.lexer.skip(1)

# Construyendo el analizador lexico
import ply.lex as lex
lexer = lex.lex()

# Presedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV'),
    ('right', 'UMENOS')
)

# Definicion de la gramatica

def p_instrucciones(t):
    '''
    instrucciones : instruccion instrucciones
                    | instruccion
    '''

def p_instruccion(t):
    '''
    instruccion : ROPERAR CORA expresion CORC PTCOMA 
    '''
    print('El resultado es: ' + str(t[3]))

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
    '''
    if t[2] == '+': t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS
    '''
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    '''
    expresion : PARA expresion PARC
    '''
    t[0] = t[2]

def p_expresion_primitivo(t):
    '''
    expresion : ENTERO
            | DECIMAL
    '''
    t[0] = t[1]

def p_error(t):
    print('Error sintactico en: ' + str(t.value))
    # almacenamiento de errores sintacticos

import ply.yacc as yacc
parser = yacc.yacc()

f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)
print("Archivo ejecutado correctamente :D")