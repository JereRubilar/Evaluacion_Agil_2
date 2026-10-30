class Producto:
    def __init__(self, nombre, stock, stock_minimo, precio=0.0, id_producto=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.precio = precio

    def en_stock_minimo(self):
        return self.stock <= self.stock_minimo

    def __str__(self):
        alerta = "  <-- STOCK MÍNIMO" if self.en_stock_minimo() else ""
        id_fmt = f"ID: {self.id_producto:<4}" if self.id_producto else "ID: N/A "
        return (f"{id_fmt} | {self.nombre:<20} | Stock: {self.stock:<5} "
                f"| Mín: {self.stock_minimo:<5} | Precio: ${self.precio:,.2f}{alerta}")