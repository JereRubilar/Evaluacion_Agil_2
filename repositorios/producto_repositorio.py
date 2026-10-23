"""
Repositorio de productos.

Es la ÚNICA clase que sabe dónde y cómo se guardan los productos.
Hoy los guarda en memoria (un diccionario); para pasar a MySQL basta
con crear otra clase con los mismos métodos y entregársela al servicio.
"""


class ProductoRepositorio:
    def __init__(self):
        self.__productos = {}   # privado: codigo -> Producto

    def guardar(self, producto):
        self.__productos[producto.codigo] = producto

    def obtener(self, codigo):
        """Devuelve el producto o None si no existe."""
        return self.__productos.get(codigo)

    def existe(self, codigo):
        return codigo in self.__productos

    def listar(self):
        return list(self.__productos.values())

    def eliminar(self, codigo):
        return self.__productos.pop(codigo, None)

    def actualizar(self, producto):
        if not self.existe(producto.codigo):
            raise ValueError(f"No existe un producto con código {producto.codigo}.")
        self.__productos[producto.codigo] = producto
