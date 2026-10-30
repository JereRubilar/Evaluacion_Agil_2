
class ProductoRepositorio:
    def __init__(self):
        self.__productos = {} 

    def guardar(self, producto):
        self.__productos[producto.codigo] = producto

    def obtener(self, codigo):
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
