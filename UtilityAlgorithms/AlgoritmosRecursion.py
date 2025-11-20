from typing import List, Tuple
from Entities.Libro import Libro

class AlgoritmosRecursion:

    @staticmethod
    def encontrar_libro_mas_ligero_autor(libros: List[Libro], autor: str) -> str | None:

        libros_autor = [l for l in libros if l.autor == autor]
        if not libros_autor:
            return None

        def _recursiva_interna(lista: List[Libro]) -> Libro:
            if len(lista) == 1:
                return lista[0]

            mejor_resto = _recursiva_interna(lista[1:])

            if lista[0].peso < mejor_resto.peso:
                return lista[0]
            else:
                return mejor_resto

        libro_ligero = _recursiva_interna(libros_autor)
        return libro_ligero.isbn

    @staticmethod
    def calcular_peso_promedio_autor(libros: List[Libro], autor: str) -> float:

        libros_autor = [l for l in libros if l.autor == autor]
        if not libros_autor:
            return 0.0

        total_peso, cantidad = AlgoritmosRecursion._sumar_pesos_cola(libros_autor, 0, 0.0, 0)
        return total_peso / cantidad if cantidad > 0 else 0.0

    @staticmethod
    def _sumar_pesos_cola(libros: List[Libro], index: int, suma_acumulada: float, count_acumulado: int) -> Tuple[
        float, int]:

        if index == len(libros):
            return suma_acumulada, count_acumulado

        return AlgoritmosRecursion._sumar_pesos_cola(
            libros,
            index + 1,
            suma_acumulada + libros[index].peso,
            count_acumulado + 1
        )