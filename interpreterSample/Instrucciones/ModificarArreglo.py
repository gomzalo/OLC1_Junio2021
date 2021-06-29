from re import A
from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy


class ModificarArreglo(Instruccion):
    def __init__(self, identificador, expresiones, valor, fila, columna):
        self.identificador = identificador
        self.expresiones = expresiones
        self.valor = valor
        self.fila = fila
        self.columna = columna


    def interpretar(self, tree, table):
        value = self.valor.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        simbolo = table.getTabla(self.identificador.lower())

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        if not simbolo.getArreglo(): 
            return Excepcion("Semantico", "Variable " + self.identificador + " no es un arreglo.", self.fila, self.columna)

        if simbolo.getTipo() != self.valor.tipo:
            return Excepcion("Semantico", "Tipos de dato diferente en Modificacion de arreglo.", self.fila, self.columna)

        # BUSQUEDA DEL ARREGLO
        value = self.modificarDimensiones(tree, table, copy.copy(self.expresiones), simbolo.getValor(), value)     #RETORNA EL VALOR SOLICITADO
        if isinstance(value, Excepcion): return value

        return value

    def getNodo(self):
        nodo = NodoAST("MODIFICACION ARREGLO")
        nodo.agregarHijo(str(self.identificador))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.expresiones:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)
        nodo.agregarHijoNodo(self.valor.getNodo())
        return nodo

    def modificarDimensiones(self, tree, table, expresiones, arreglo, valor):
        if len(expresiones) == 0:
            if isinstance(arreglo, list):
                return Excepcion("Semantico", "Modificacion a Arreglo incompleto.", self.fila, self.columna)
            return valor
        if not isinstance(arreglo, list):
            return Excepcion("Semantico", "Accesos de más en un Arreglo.", self.fila, self.columna)
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        
        value = self.modificarDimensiones(tree, table, copy.copy(expresiones), arreglo[num], valor)
        if isinstance(value, Excepcion): return value
        if value != None:
            arreglo[num] = value

        return None



            

