from typing import List

from Entities.Prestamo import Prestamo
from DataStructures.Pila import Pila


class Usuario:

    def __init__(self, id_usuario: str, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.historial_prestamos = Pila()

    def prestar_libro(self, prestamo: Prestamo) -> None:
        self.historial_prestamos.apilar(prestamo)

    def ver_historial_como_lista(self) -> List[Prestamo]:
        return self.historial_prestamos.obtener_elementos_como_lista()