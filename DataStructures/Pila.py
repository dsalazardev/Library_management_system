from typing import List, Any

class Pila:

    def __init__(self):
        self._elementos: List[Any] = []

    def apilar(self, elemento: Any) -> None:
        self._elementos.append(elemento)

    def desapilar(self) -> Any | None:
        if self.esta_vacia():
            return None
        return self._elementos.pop()

    def cima(self) -> Any | None:
        if self.esta_vacia():
            return None
        return self._elementos[-1]

    def esta_vacia(self) -> bool:
        return len(self._elementos) == 0

    def obtener_elementos_como_lista(self) -> List[Any]:
        return self._elementos.copy()