import sys
import os

from Controller.Biblioteca import Biblioteca
from Entities.Libro import Libro


def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        if 'TERM' not in os.environ:
            print("\n" * 100)
        else:
            os.system('clear')


def imprimir_encabezado():
    print("=" * 60)
    print("      SISTEMA DE GESTIÓN DE BIBLIOTECAS (SGB) 2025-2")
    print("           Facultad de IA e Ingenierías")
    print("=" * 60)


def precargar_datos_prueba(biblio: Biblioteca):
    print(">> Cargando datos de prueba...")

    # 1. Crear Usuarios
    biblio.crear_usuario("U001", "Mario Bravo")
    biblio.crear_usuario("U002", "Ana Maria")
    biblio.crear_usuario("U003", "Juan Perez")

    libros = [
        Libro("978-1", "Cien años de soledad", "Gabriel Garcia Marquez", 0.4, 50000, 1),
        # Peso < 0.5 (Para probar Poda)
        Libro("978-2", "El Amor en los tiempos del colera", "Gabriel Garcia Marquez", 0.6, 45000, 2),
        Libro("978-3", "Estructuras de Datos en Python", "Dr. Algoritmo", 1.2, 120000, 0),
        # Stock 0 (Para probar Pila de Espera)
        Libro("978-4", "Inteligencia Artificial Moderna", "Stuart Russell", 2.5, 250000, 1),
        Libro("978-5", "Clean Code", "Robert C. Martin", 0.8, 180000, 3),
        Libro("978-6", "El Principito", "Antoine de Saint-Exupéry", 0.2, 30000, 5)  # Peso muy bajo
    ]

    for l in libros:
        biblio.agregar_libro(l)

    print(">> Datos cargados exitosamente.\n")


def menu_principal():
    biblio = Biblioteca()
    precargar_datos_prueba(biblio)

    while True:
        imprimir_encabezado()
        print("1. Gestión de Usuarios (Crear/Buscar)")
        print("2. Gestión de Préstamos y Devoluciones")
        print("3. Consultas y Búsquedas (Lineal/Binaria)")
        print("4. Reportes (Ordenamientos Merge/Insertion)")
        print("5. Módulo Estantería (Backtracking/Fuerza Bruta)")
        print("6. Estadísticas de Autor (Recursión)")
        print("7. Cargar desde Archivo (CSV/JSON)")
        print("0. Salir")
        print("-" * 60)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_usuarios(biblio)
        elif opcion == "2":
            gestionar_transacciones(biblio)
        elif opcion == "3":
            gestionar_busquedas(biblio)
        elif opcion == "4":
            gestionar_reportes(biblio)
        elif opcion == "5":
            gestionar_estanteria(biblio)
        elif opcion == "6":
            gestionar_recursion(biblio)
        elif opcion == "7":
            ruta = input("Ingrese la ruta del archivo (ej: datos.csv): ")
            resultado = biblio.cargar_datos_desde_archivo(ruta)
            print(resultado)
            input("Presione Enter para continuar...")
        elif opcion == "0":
            print("Saliendo del sistema...")
            sys.exit()
        else:
            print("Opción inválida.")
            input("Enter para continuar...")

        limpiar_pantalla()


def gestionar_usuarios(biblio: Biblioteca):
    print("\n--- GESTIÓN DE USUARIOS ---")
    id_user = input("ID Usuario: ")
    nombre = input("Nombre (dejar vacío si solo busca): ")

    if nombre:
        print(biblio.crear_usuario(id_user, nombre))
    else:
        user = biblio.buscar_usuario(id_user)
        if user:
            print(f"Usuario encontrado: {user.nombre}")
        else:
            print("Usuario no existe.")
    input("Enter para volver...")


def gestionar_transacciones(biblio: Biblioteca):
    print("\n--- PRÉSTAMOS Y DEVOLUCIONES ---")
    print("1. Prestar Libro")
    print("2. Devolver Libro (Activa Lógica de Reservas LIFO)")
    op = input("Opción: ")

    id_user = input("ID Usuario: ")
    isbn = input("ISBN del Libro: ")

    if op == "1":
        # Aquí se prueba la Pila de Espera si el stock es 0
        resultado = biblio.gestionar_prestamo(id_user, isbn)
        print(f"\nRESULTADO: {resultado}")
    elif op == "2":
        # Aquí se prueba la asignación automática a la reserva
        resultado = biblio.gestionar_devolucion(id_user, isbn)
        print(f"\nRESULTADO: {resultado}")

    input("Enter para volver...")


def gestionar_busquedas(biblio: Biblioteca):
    print("\n--- BÚSQUEDAS ---")
    print("1. Búsqueda Lineal (Por Título)")
    print("2. Búsqueda Lineal (Por Autor)")
    op = input("Opción: ")
    query = input("Texto a buscar: ")

    por_autor = (op == "2")
    resultados = biblio.buscar_libro_lineal(query, "autor" if por_autor else "titulo")

    print(f"\nEncontrados {len(resultados)} libros:")
    for libro in resultados:
        print(f" - {libro.obtener_info_completa()}")
    input("Enter para volver...")


def gestionar_reportes(biblio: Biblioteca):
    print("\n--- REPORTES ---")
    print("1. Inventario Global por Valor (Merge Sort)")
    print("2. Historial de un Usuario por Fecha (Insertion Sort - MODIFICACIÓN 2)")
    op = input("Opción: ")

    if op == "1":
        lista = biblio.generar_reporte_valor()
        print("\nLibros ordenados por Valor (COP):")
        for l in lista:
            print(f" ${l.valor} - {l.titulo}")

    elif op == "2":
        id_user = input("ID Usuario a consultar: ")
        historial = biblio.generar_reporte_historial_usuario(id_user)
        print(f"\nHistorial de {id_user} ordenado por Fecha:")
        if not historial:
            print(" (Historial vacío)")
        for prestamo in historial:
            print(f" {prestamo.fecha} - Libro ISBN: {prestamo.isbn}")

    input("Enter para volver...")


def gestionar_estanteria(biblio: Biblioteca):
    print("\n--- MÓDULO ESTANTERÍA ---")
    print("1. Fuerza Bruta (Combos > 8kg)")
    print("2. Backtracking Óptimo (Max Valor, Max 8kg, Poda < 0.5kg - MODIFICACIÓN 3)")
    op = input("Opción: ")

    if op == "1":
        combos = biblio.resolver_estanteria_sobrepeso()
        print(f"\nSe encontraron {len(combos)} combinaciones peligrosas.")
        for i, c in enumerate(combos):
            print(f"Combo {i + 1}: {[l.titulo for l in c]}")

    elif op == "2":
        print("Calculando la mejor selección de libros...")
        seleccion = biblio.resolver_estanteria_optima(max_peso=8.0)
        total_valor = sum(l.valor for l in seleccion)
        total_peso = sum(l.peso for l in seleccion)

        print(f"\n--- MEJOR SELECCIÓN ENCONTRADA ---")
        print(f"Valor Total: ${total_valor}")
        print(f"Peso Total: {total_peso:.2f} kg")
        print("Libros:")
        for l in seleccion:
            print(f" - {l.titulo} (${l.valor}, {l.peso}kg)")
        print("\nNOTA: Si falta 'Cien años de soledad' (0.4kg), es por la PODA (<0.5kg).")

    input("Enter para volver...")


def gestionar_recursion(biblio: Biblioteca):
    print("\n--- ALGORITMOS RECURSIVOS ---")
    autor = input("Nombre exacto del Autor (ej: Gabriel Garcia Marquez): ")

    print("\n1. Libro más ligero (Recursión Pila - MODIFICACIÓN 1)")
    isbn_ligero = biblio.buscar_libro_mas_ligero_por_autor(autor)
    print(f"   ISBN del libro más ligero: {isbn_ligero}")

    print("\n2. Peso promedio (Recursión Cola)")
    promedio = biblio.calcular_peso_promedio_por_autor(autor)
    print(f"   Peso promedio de sus libros: {promedio:.2f} kg")

    input("Enter para volver...")


if __name__ == "__main__":
    menu_principal()