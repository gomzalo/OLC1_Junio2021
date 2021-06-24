from Abstract.NodoAST import NodoAST
from Abstract.Instruccion import Instruccion
from TS.Tipo import TIPO

class Read(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.CADENA

    def interpretar(self, tree, table):
        print(tree.getConsola()) #IMPRIME LA CONSOLA
        print("Ingreso a un READ. Ingrese el valor")
        tree.setConsola("")     #RESETEA LA CONSOLA
        # ESTO SOLO ES DE EJEMPLO
        lectura = input() # OBTENERME EL VALOR INGRESADO
        return lectura

    def getNodo(self):
        nodo = NodoAST("READ")
        return nodo