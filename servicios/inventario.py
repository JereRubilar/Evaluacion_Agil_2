from modelos import Movimiento, Producto
from repositorios import MovimientoRepositorio, ProductoRepositorio


class Inventario:
    def __init__(self, repo_productos=None, repo_movimientos=None):
        self.__productos = repo_productos or ProductoRepositorio()
        self.__movimientos = repo_movimientos or MovimientoRepositorio()

    def buscar(self, id_producto):
        producto = self.__productos.obtener(id_producto)
        if producto is None:
            raise ValueError(f"No existe un producto con ID {id_producto}.")
        return producto

    def listar(self):
        return self.__productos.listar()

    # ---------- HU01: ingresar producto ----------
    def agregar_producto(self, nombre, stock_inicial, stock_minimo, precio=0.0):
        if not nombre:
            raise ValueError("El nombre del producto es obligatorio.")
        if stock_inicial < 0 or stock_minimo < 0:
            raise ValueError("El stock no puede ser negativo.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        
        producto = Producto(nombre=nombre, stock=stock_inicial, stock_minimo=stock_minimo, precio=precio)
        self.__productos.guardar(producto)
        return producto

    # ---------- HU02 y HU05: entradas de stock ----------
    def registrar_alta(self, id_producto, cantidad, id_usuario, detalle=""):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        producto = self.buscar(id_producto)
        producto.stock += cantidad
        self.__productos.actualizar(producto)
        
        movimiento = Movimiento(
            id_producto=id_producto,
            tipo=Movimiento.ALTA,
            cantidad=cantidad,
            id_usuario=id_usuario
        )
        self.__movimientos.guardar(movimiento)
        return producto

    # ---------- HU03: salidas de stock ----------
    def registrar_baja(self, id_producto, cantidad, id_usuario, detalle=""):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        producto = self.buscar(id_producto)
        if cantidad > producto.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}.")
        producto.stock -= cantidad
        self.__productos.actualizar(producto)
        
        movimiento = Movimiento(
            id_producto=id_producto,
            tipo=Movimiento.BAJA,
            cantidad=cantidad,
            id_usuario=id_usuario
        )
        self.__movimientos.guardar(movimiento)
        return producto

    # ---------- HU04: modificar producto ----------
    def modificar_producto(self, id_producto, nombre=None, precio=None, stock_minimo=None):
        producto = self.buscar(id_producto)
        if precio is not None and precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock_minimo is not None and stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        
        if nombre:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if stock_minimo is not None:
            producto.stock_minimo = stock_minimo
            
        self.__productos.actualizar(producto)
        return producto

    # ---------- HU06: alerta de stock mínimo ----------
    def productos_en_alerta(self):
        return [p for p in self.__productos.listar() if p.en_stock_minimo()]

    # ---------- HU07: historial ----------
    def historial(self, id_producto):
        self.buscar(id_producto)   # valida que exista
        return self.__movimientos.listar_por_producto(id_producto)

    # ---------- HU08: eliminar producto ----------
    def eliminar_producto(self, id_producto):
        producto = self.buscar(id_producto)
        self.__productos.eliminar(id_producto)
        self.__movimientos.eliminar_por_producto(id_producto)
        return producto