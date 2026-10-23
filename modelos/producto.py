"""Modelo Producto."""


class Producto:
    def __init__(self, codigo, nombre, stock_inicial, stock_minimo, precio=0):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock_inicial
        self.stock_minimo = stock_minimo
        self.precio = precio

    def en_stock_minimo(self):
        """HU06: True si el stock llegó o bajó del mínimo."""
        return self.stock <= self.stock_minimo

    def __str__(self):
        alerta = "  <-- STOCK MÍNIMO" if self.en_stock_minimo() else ""
        return (f"{self.codigo:<8} {self.nombre:<20} Stock: {self.stock:<5} "
                f"Mín: {self.stock_minimo:<5} Precio: ${self.precio:,}{alerta}")
