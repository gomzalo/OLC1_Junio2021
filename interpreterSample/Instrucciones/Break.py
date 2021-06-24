from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoAST("BREAK")
        return nodo