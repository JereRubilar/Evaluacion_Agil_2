class Producto:
    def __init__(self, nombre, stock, stock_minimo, precio=0.0, id_categoria=None, id_producto=None, nombre_categoria=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.precio = precio
        self.id_categoria = id_categoria
        self.nombre_categoria = nombre_categoria

    def en_stock_minimo(self):
        return self.stock <= self.stock_minimo

    def __str__(self):
        alerta = "  <-- STOCK MÍNIMO" if self.en_stock_minimo() else ""
        id_fmt = f"ID: {self.id_producto:<4}" if self.id_producto else "ID: N/A "
        cat_fmt = f" | Cat: {self.nombre_categoria or self.id_categoria or 'Sin Cat.'}"
        return (f"{id_fmt} | {self.nombre:<20}{cat_fmt} | Stock: {self.stock:<5} "
                f"| Mín: {self.stock_minimo:<5} | Precio: ${self.precio:,.2f}{alerta}")