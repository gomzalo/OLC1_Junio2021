from re import A
from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy


class DeclaracionArr1(Instruccion):
    def __init__(self, tipo1, dimensiones, identificador, tipo2, expresiones, fila, columna):
        self.identificador = identificador
        self.tipo = tipo1
        self.tipo2 = tipo2
        self.dimensiones = dimensiones
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.arreglo = True


    def interpretar(self, tree, table):
        if self.tipo != self.tipo2:                     #VERIFICACION DE TIPOS
            return Excepcion("Semantico", "Tipo de dato diferente en Arreglo.", self.fila, self.columna)
        if self.dimensiones != len(self.expresiones):   #VERIFICACION DE DIMENSIONES
            return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)

        # CREACION DEL ARREGLO
        value = self.crearDimensiones(tree, table, copy.copy(self.expresiones))     #RETORNA EL ARREGLO DE DIMENSIONES
        if isinstance(value, Excepcion): return value
        simbolo = Simbolo(str(self.identificador), self.tipo, self.arreglo, self.fila, self.columna, value)
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        return None

    def getNodo(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijo(str(self.dimensiones))
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijo(str(self.tipo2))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.expresiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        return nodo

    def crearDimensiones(self, tree, table, expresiones):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(expresiones)))
            contador += 1
        return arr



            

