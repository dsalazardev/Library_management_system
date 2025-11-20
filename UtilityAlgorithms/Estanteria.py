from Entities.Libro import Libro
from typing import List


class Estanteria:

    @staticmethod
    def encontrar_combinaciones_sobrepeso(libros: List[Libro], k: int = 4, umbral: float = 8.0) -> List[List[Libro]]:
        import itertools
        resultados = []
        for combinacion in itertools.combinations(libros, k):
            peso_total = sum(l.peso for l in combinacion)
            if peso_total > umbral:
                resultados.append(list(combinacion))
        return resultados

    @staticmethod
    def encontrar_estanteria_optima(libros: List[Libro], max_peso: float = 8.0) -> List[Libro]:

        return Estanteria._backtrack_optimo(libros, max_peso, 0, [], 0.0, 0.0)

    @staticmethod
    def _backtrack_optimo(libros: List[Libro], max_peso: float, index: int,
                          camino_actual: List[Libro], peso_actual: float, valor_actual: float) -> List[Libro]:

        if index == len(libros):
            return camino_actual

        mejor_camino = camino_actual
        mejor_valor = valor_actual

        for i in range(index, len(libros)):
            libro = libros[i]

            if libro.peso < 0.5:
                continue  # Skip this branch entirely

            if peso_actual + libro.peso <= max_peso:

                camino_candidato = Estanteria._backtrack_optimo(
                    libros,
                    max_peso,
                    i + 1,
                    camino_actual + [libro],
                    peso_actual + libro.peso,
                    valor_actual + libro.valor
                )

                valor_candidato = sum(l.valor for l in camino_candidato)
                if valor_candidato > mejor_valor:
                    mejor_valor = valor_candidato
                    mejor_camino = camino_candidato

        return mejor_camino