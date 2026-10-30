
class MovimientoRepositorio:
    def __init__(self):
        self.__movimientos = []

    def guardar(self, codigo_producto, movimiento):
        self.__movimientos.append((codigo_producto, movimiento))

    def listar_por_producto(self, codigo_producto):
        return [m for codigo, m in self.__movimientos if codigo == codigo_producto]

    def eliminar_por_producto(self, codigo_producto):
        self.__movimientos = [(c, m) for c, m in self.__movimientos if c != codigo_producto]
