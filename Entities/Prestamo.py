from datetime import date

class Prestamo:

    def __init__(self, isbn: str, fecha: date):
        self.isbn = isbn
        self.fecha = fecha

    def obtener_info(self) -> str:
        return f"Loan - ISBN: {self.isbn}, Date: {self.fecha}"

    def __repr__(self):
        return f"<Prestamo {self.fecha}>"