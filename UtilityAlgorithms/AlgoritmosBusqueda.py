from typing import List

from Entities.Libro import Libro

class AlgoritmosBusqueda:

    @staticmethod
    def busqueda_lineal(inventario: List[Libro], query: str, por_autor: bool) -> List[Libro]:

        resultados = []
        query_norm = query.lower()
        for libro in inventario:
            target = libro.autor.lower() if por_autor else libro.titulo.lower()
            if query_norm in target:
                resultados.append(libro)
        return resultados

    @staticmethod
    def busqueda_binaria_isbn(inventario_ordenado: List[Libro], isbn: str) -> int | None:

        low = 0
        high = len(inventario_ordenado) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_isbn = inventario_ordenado[mid].isbn

            if mid_isbn == isbn:
                return mid
            elif mid_isbn < isbn:
                low = mid + 1
            else:
                high = mid - 1
        return None