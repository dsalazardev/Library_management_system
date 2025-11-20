from typing import Dict
from DataStructures.Pila import Pila

class PilaDeEspera:

    def __init__(self):
        self.reservas_por_isbn: Dict[str, Pila] = {}

    def apilar_reserva(self, isbn: str, id_usuario: str) -> None:

        if isbn not in self.reservas_por_isbn:
            self.reservas_por_isbn[isbn] = Pila()
        self.reservas_por_isbn[isbn].apilar(id_usuario)

    def desapilar_reserva(self, isbn: str) -> str | None:

        if isbn in self.reservas_por_isbn:
            usuario = self.reservas_por_isbn[isbn].desapilar()
            if self.reservas_por_isbn[isbn].esta_vacia():
                del self.reservas_por_isbn[isbn]
            return usuario
        return None

    def hay_reservas(self, isbn: str) -> bool:
        return isbn in self.reservas_por_isbn and not self.reservas_por_isbn[isbn].esta_vacia()

    def total_reservas_para_libro(self, isbn: str) -> int:
        if isbn in self.reservas_por_isbn:
             return len(self.reservas_por_isbn[isbn].obtener_elementos_como_lista())
        return 0