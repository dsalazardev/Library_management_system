import csv
import json
import os
from typing import List, Dict, Optional
from datetime import date

from Entities.Libro import Libro
from Entities.Prestamo import Prestamo
from DataStructures.Usuario import Usuario
from DataStructures.PilaDeEspera import PilaDeEspera

from UtilityAlgorithms.AlgoritmosOrdenamiento import AlgoritmosOrdenamiento
from UtilityAlgorithms.AlgoritmosBusqueda import AlgoritmosBusqueda
from UtilityAlgorithms.Estanteria import Estanteria
from UtilityAlgorithms.AlgoritmosRecursion import AlgoritmosRecursion


class Biblioteca:

    def __init__(self):

        self.inventario_general: List[Libro] = []
        self.inventario_ordenado_isbn: List[Libro] = []

        self.usuarios: Dict[str, Usuario] = {}
        self.reservas_espera = PilaDeEspera()

        self._ordenador = AlgoritmosOrdenamiento()
        self._buscador = AlgoritmosBusqueda()
        self._estanteria = Estanteria()
        self._recursor = AlgoritmosRecursion()


    # A. GESTIÓN DE DATOS E INVENTARIO

    def cargar_datos_desde_archivo(self, ruta: str) -> str:

        if not os.path.exists(ruta):
            return f"Error: File {ruta} not found."

        try:
            if ruta.endswith('.csv'):
                with open(ruta, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        print(f"Row: {row}")
                        libro = Libro(
                            isbn=row['isbn'],
                            titulo=row['titulo'],
                            autor=row['autor'],
                            peso=float(row['peso']),
                            valor=float(row['valor']),
                            stock=int(row['stock'])
                        )
                        self.agregar_libro(libro)

            elif ruta.endswith('.json'):
                with open(ruta, mode='r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        libro = Libro(
                            isbn=item['isbn'],
                            titulo=item['titulo'],
                            autor=item['autor'],
                            peso=float(item['peso']),
                            valor=float(item['valor']),
                            stock=int(item['stock'])
                        )
                        self.agregar_libro(libro)
            else:
                return "Error: Unsupported file format. Use .csv or .json"

            return "Data loaded successfully."
        except Exception as e:
            return f"Error loading data: {str(e)}"

    def agregar_libro(self, libro: Libro) -> None:
        self.inventario_general.append(libro)

        self.inventario_ordenado_isbn.append(libro)
        self.inventario_ordenado_isbn.sort(key=lambda x: x.isbn)

        # Opción B (Más estricta con requisitos previos):
        # self._ordenador.insertar_libro_en_orden_isbn(self.inventario_ordenado_isbn, libro)

    # B. GESTIÓN DE USUARIOS

    def crear_usuario(self, id_usuario: str, nombre: str) -> str:
        if id_usuario in self.usuarios:
            return "Error: User ID already exists."
        self.usuarios[id_usuario] = Usuario(id_usuario, nombre)
        return "Usuario creado exitosamente."

    def buscar_usuario(self, id_usuario: str) -> Usuario | None:
        return self.usuarios.get(id_usuario)

    # C. PRÉSTAMOS, DEVOLUCIONES Y RESERVAS

    def gestionar_prestamo(self, id_usuario: str, isbn: str) -> str:

        user = self.buscar_usuario(id_usuario)
        if not user:
            return "Error: Usuario no encontrado."

        idx = self._buscador.busqueda_binaria_isbn(self.inventario_ordenado_isbn, isbn)
        if idx is None:
            return "Error: Libro no encontrado en el inventario."

        libro = self.inventario_ordenado_isbn[idx]

        if libro.esta_disponible():
            libro.decrementar_stock()
            prestamo = Prestamo(isbn, date.today())
            user.prestar_libro(prestamo)
            return f"Préstamo exitoso: '{libro.titulo}' entregado a {user.nombre}."
        else:
            # 3. Stock 0 -> Gestionar Reserva en Pila (Modificación 4)
            self.reservas_espera.apilar_reserva(isbn, id_usuario)
            return "Libro sin stock. Usuario agregado a la LISTA DE ESPERA (Pila LIFO)."


    def gestionar_devolucion(self, id_usuario: str, isbn: str) -> str:

        idx = self._buscador.busqueda_binaria_isbn(self.inventario_ordenado_isbn, isbn)
        if idx is None: return "Error crítico: Libro no existe en inventario."

        libro = self.inventario_ordenado_isbn[idx]
        libro.incrementar_stock()

        if self.reservas_espera.hay_reservas(isbn):
            next_user_id = self.reservas_espera.desapilar_reserva(isbn)

            if next_user_id:
                # Asignación automática (reducir stock de nuevo y prestar)
                libro.decrementar_stock()
                next_user = self.buscar_usuario(next_user_id)
                if next_user:
                    nuevo_prestamo = Prestamo(isbn, date.today())
                    next_user.prestar_libro(nuevo_prestamo)
                    return f"Devolución registrada. Libro asignado inmediatamente a reserva prioritaria: Usuario {next_user.nombre}."

        return "Devolución exitosa. El libro vuelve a estar disponible."

    def gestionar_reserva(self, id_usuario: str, isbn: str) -> str:

        idx = self._buscador.busqueda_binaria_isbn(self.inventario_ordenado_isbn, isbn)
        if idx is None: return "Libro no encontrado."

        libro = self.inventario_ordenado_isbn[idx]

        if libro.stock > 0:
            return "Error: No se puede reservar. Hay copias disponibles, solicite un préstamo."

        self.reservas_espera.apilar_reserva(isbn, id_usuario)
        return "Reserva agregada exitosamente (Pila de espera)."

    # D. REPORTES Y BÚSQUEDAS (Wrappers de Algoritmos)

    def buscar_libro_lineal(self, query: str, por: str = 'titulo') -> List[Libro]:
        buscar_por_autor = (por.lower() == 'autor')
        return self._buscador.busqueda_lineal(self.inventario_general, query, buscar_por_autor)

    def generar_reporte_valor(self) -> List[Libro]:
        return self._ordenador.merge_sort_por_valor(self.inventario_general)

    def generar_reporte_historial_usuario(self, id_usuario: str) -> List[Prestamo]:

        user = self.buscar_usuario(id_usuario)

        if user:
            return self._ordenador.ordenar_historial_por_insercion_fecha(user.historial_prestamos)
        return []

    # E. RESOLUCIÓN DE PROBLEMAS Y RECURSIÓN

    def resolver_estanteria_sobrepeso(self) -> List[List[Libro]]:
        return self._estanteria.encontrar_combinaciones_sobrepeso(self.inventario_general, k=4, umbral=8.0)

    def resolver_estanteria_optima(self, max_peso: float = 8.0) -> List[Libro]:
        return self._estanteria.encontrar_estanteria_optima(self.inventario_general, max_peso)

    def buscar_libro_mas_ligero_por_autor(self, autor: str) -> Libro | None:
        return self._recursor.encontrar_libro_mas_ligero_autor(self.inventario_general, autor)

    def calcular_peso_promedio_por_autor(self, autor: str) -> float:
        return self._recursor.calcular_peso_promedio_autor(self.inventario_general, autor)