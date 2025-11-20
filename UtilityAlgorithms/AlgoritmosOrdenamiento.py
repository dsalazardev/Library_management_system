from typing import List

from Entities.Libro import Libro
from Entities.Prestamo import Prestamo
from DataStructures.Pila import Pila

class AlgoritmosOrdenamiento:

    @staticmethod
    def merge_sort_por_valor(libros: List[Libro]) -> List[Libro]:

        if len(libros) <= 1:
            return libros

        mid = len(libros) // 2
        left = AlgoritmosOrdenamiento.merge_sort_por_valor(libros[:mid])
        right = AlgoritmosOrdenamiento.merge_sort_por_valor(libros[mid:])

        return AlgoritmosOrdenamiento._merge_valor(left, right)

    @staticmethod
    def _merge_valor(left: List[Libro], right: List[Libro]) -> List[Libro]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i].valor <= right[j].valor:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def insertion_sort_por_fecha(prestamos: List[Prestamo]) -> List[Prestamo]:

        for i in range(1, len(prestamos)):
            key_item = prestamos[i]
            j = i - 1
            while j >= 0 and prestamos[j].fecha > key_item.fecha:
                prestamos[j + 1] = prestamos[j]
                j -= 1
            prestamos[j + 1] = key_item
        return prestamos

    @staticmethod
    def ordenar_historial_por_insercion_fecha(pila_historial: Pila) -> List[Prestamo]:

        lista = pila_historial.obtener_elementos_como_lista()
        return AlgoritmosOrdenamiento.insertion_sort_por_fecha(lista)