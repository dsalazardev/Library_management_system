class Libro:

    def __init__(self, isbn: str, titulo: str, autor: str, peso: float, valor: float, stock: int):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.peso = peso
        self.valor = valor
        self.stock = stock

    def obtener_info_completa(self) -> str:
        return f"ISBN: {self.isbn}, Title: {self.titulo}, Author: {self.autor}, Weight: {self.peso}kg, Value: ${self.valor}, Stock: {self.stock}"

    def esta_disponible(self) -> bool:
        return self.stock > 0

    def decrementar_stock(self) -> None:
        if self.stock > 0:
            self.stock -= 1

    def incrementar_stock(self) -> None:
        self.stock += 1

    def __repr__(self):
        return f"<Libro {self.isbn}>"