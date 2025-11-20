import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.Biblioteca import Biblioteca
from Entities.Libro import Libro

ANCHO = 900
ALTO = 700
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (240, 240, 240)
GRIS_OSCURO = (50, 50, 50)
AZUL = (0, 120, 215)
VERDE = (0, 153, 51)
ROJO = (204, 0, 0)

class Boton:
    def __init__(self, x, y, w, h, texto, color_base, accion=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = (min(color_base[0] + 30, 255), min(color_base[1] + 30, 255), min(color_base[2] + 30, 255))
        self.accion = accion
        self.font = pygame.font.SysFont('Arial', 18, bold=True)

    def dibujar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_base

        pygame.draw.rect(superficie, color, self.rect, border_radius=8)
        pygame.draw.rect(superficie, NEGRO, self.rect, 2, border_radius=8)

        texto_render = self.font.render(self.texto, True, BLANCO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, texto_rect)

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                if self.accion:
                    return self.accion()
        return None


class CajaTexto:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactivo = pygame.Color('lightskyblue3')
        self.color_activo = pygame.Color('dodgerblue2')
        self.color = self.color_inactivo
        self.texto = ""
        self.placeholder = placeholder
        self.font = pygame.font.SysFont('Arial', 18)
        self.activo = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.activo = not self.activo
            else:
                self.activo = False
            self.color = self.color_activo if self.activo else self.color_inactivo

        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_RETURN:
                    return self.texto  # Retorna texto al dar Enter
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                else:
                    self.texto += evento.unicode
        return None

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, BLANCO, self.rect)

        texto_mostrar = self.texto if self.texto else self.placeholder
        color_texto = NEGRO if self.texto else (150, 150, 150)

        txt_surface = self.font.render(texto_mostrar, True, color_texto)
        superficie.blit(txt_surface, (self.rect.x + 5, self.rect.y + 10))
        pygame.draw.rect(superficie, self.color, self.rect, 2)

class VistaSGB:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("SGB 2025-2 - Sistema de Biblioteca")
        self.reloj = pygame.time.Clock()
        self.font_titulo = pygame.font.SysFont('Arial', 28, bold=True)
        self.font_res = pygame.font.SysFont('Consolas', 14)

        self.biblio = Biblioteca()
        self.precargar_datos()

        self.resultado_texto = ["Bienvenido al SGB.", "Seleccione una opción a la izquierda."]
        self.input_activo = None

        self.botones = []
        self.inputs = []
        self.crear_interfaz()

    def precargar_datos(self):
        # Mismos datos que tu Main.py
        self.biblio.crear_usuario("U001", "Mario Bravo")
        self.biblio.crear_usuario("U002", "Ana Maria")
        libros = [
            Libro("978-1", "Cien años de soledad", "Gabo", 0.4, 50000, 1),
            Libro("978-3", "Python Data Structures", "Dr. A", 1.2, 120000, 0),  # Stock 0
            Libro("978-4", "IA Moderna", "Russell", 2.5, 250000, 1)
        ]
        for l in libros: self.biblio.agregar_libro(l)

    def crear_interfaz(self):
        # Panel Izquierdo (Botones)
        y_start = 80
        gap = 50

        btns = [
            ("1. Reporte Valor (MergeSort)", AZUL, self.accion_reporte_valor),
            ("2. Buscar Libro (Lineal)", AZUL, self.activar_busqueda),
            ("3. Estantería Óptima (Backtrack)", VERDE, self.accion_estanteria),
            ("4. Prestar Libro (Stock 0 test)", ROJO, self.activar_prestamo),
            ("5. Devolver (Test Cola LIFO)", ROJO, self.activar_devolucion),
            ("6. Recursión (Autor)", VERDE, self.activar_recursion)
        ]

        for i, (txt, col, func) in enumerate(btns):
            self.botones.append(Boton(20, y_start + (i * gap), 280, 40, txt, col, func))

        self.caja_input_1 = CajaTexto(320, 80, 200, 40, "ID / Autor")
        self.caja_input_2 = CajaTexto(540, 80, 200, 40, "ISBN / Query")
        self.btn_confirmar = Boton(760, 80, 100, 40, "OK", GRIS_OSCURO, self.procesar_input)

        self.inputs = [self.caja_input_1, self.caja_input_2]

        self.modo_actual = "INFO"  # INFO, PRESTAMO, BUSQUEDA, ETC.


    def mostrar_resultado(self, lineas):
        if isinstance(lineas, str):
            self.resultado_texto = [lineas]
        else:
            self.resultado_texto = lineas

    def accion_reporte_valor(self):
        self.modo_actual = "INFO"
        lista = self.biblio.generar_reporte_valor()
        res = ["--- REPORTE POR VALOR (MERGE SORT) ---"]
        for l in lista:
            res.append(f"${l.valor} - {l.titulo}")
        self.mostrar_resultado(res)

    def accion_estanteria(self):
        self.modo_actual = "INFO"
        sel = self.biblio.resolver_estanteria_optima(8.0)
        res = ["--- ESTANTERÍA ÓPTIMA (BACKTRACKING) ---", "Max 8kg, Poda < 0.5kg", ""]
        total = 0
        for l in sel:
            res.append(f"* {l.titulo} ({l.peso}kg)")
            total += l.valor
        res.append(f"\nValor Total: ${total}")
        self.mostrar_resultado(res)

    def activar_busqueda(self):
        self.modo_actual = "BUSCAR"
        self.mostrar_resultado(["INGRESE DATOS ARRIBA:", "Caja 1: (Ignorar)", "Caja 2: Título a buscar", "Presione OK"])

    def activar_prestamo(self):
        self.modo_actual = "PRESTAR"
        self.mostrar_resultado(["INGRESE DATOS ARRIBA:", "Caja 1: ID Usuario", "Caja 2: ISBN Libro", "Presione OK"])

    def activar_devolucion(self):
        self.modo_actual = "DEVOLVER"
        self.mostrar_resultado(["INGRESE DATOS ARRIBA:", "Caja 1: ID Usuario", "Caja 2: ISBN Libro", "Presione OK"])

    def activar_recursion(self):
        self.modo_actual = "RECURSION"
        self.mostrar_resultado(
            ["INGRESE DATOS ARRIBA:", "Caja 1: (Ignorar)", "Caja 2: Nombre Autor Exacto", "Presione OK"])

    def procesar_input(self):
        val1 = self.caja_input_1.texto
        val2 = self.caja_input_2.texto

        if self.modo_actual == "BUSCAR":
            res = self.biblio.buscar_libro_lineal(val2, "titulo")
            txt = [f"Resultados para '{val2}':"] + [l.obtener_info_completa() for l in res]
            self.mostrar_resultado(txt)

        elif self.modo_actual == "PRESTAR":
            msg = self.biblio.gestionar_prestamo(val1, val2)
            self.mostrar_resultado([f"Intento Préstamo {val1} -> {val2}", "", msg])

        elif self.modo_actual == "DEVOLVER":
            msg = self.biblio.gestionar_devolucion(val1, val2)
            self.mostrar_resultado([f"Devolución {val1} -> {val2}", "", msg])

        elif self.modo_actual == "RECURSION":
            isbn = self.biblio.encontrar_libro_ligero_autor(val2)
            prom = self.biblio.calcular_peso_promedio_por_autor(val2)
            self.mostrar_resultado(
                [f"Autor: {val2}", f"Libro más ligero (ISBN): {isbn}", f"Peso Promedio: {prom:.2f} kg"])

    # --- LOOP PRINCIPAL ---

    def correr(self):
        while True:
            self.pantalla.fill(GRIS_CLARO)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()

                for b in self.botones: b.click(event)
                self.btn_confirmar.click(event)
                for i in self.inputs: i.manejar_evento(event)

            # Dibujar Título
            titulo = self.font_titulo.render("SGB - Biblioteca Inteligente", True, NEGRO)
            self.pantalla.blit(titulo, (20, 20))

            # Dibujar Botones
            for b in self.botones: b.dibujar(self.pantalla)
            self.btn_confirmar.dibujar(self.pantalla)

            # Dibujar Inputs
            for i in self.inputs: i.dibujar(self.pantalla)

            # Dibujar Área de Resultados (Panel Negro)
            pygame.draw.rect(self.pantalla, NEGRO, (320, 150, 560, 500), border_radius=10)
            y_text = 170
            for linea in self.resultado_texto:
                color_linea = VERDE if "exitoso" in linea.lower() or "asignado" in linea.lower() else BLANCO
                render = self.font_res.render(linea, True, color_linea)
                self.pantalla.blit(render, (340, y_text))
                y_text += 25

            pygame.display.flip()
            self.reloj.tick(60)


if __name__ == "__main__":
    app = VistaSGB()
    app.correr()