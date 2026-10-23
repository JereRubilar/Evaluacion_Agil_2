"""
Servicio de inventario: reglas de negocio de las historias de usuario.

No guarda datos por sí mismo; todo lo pide a los repositorios.
"""

from Evaluacion_Agil_2.modelos import Movimiento, Producto
from Evaluacion_Agil_2.repositorios import MovimientoRepositorio, ProductoRepositorio


class Inventario:
    def __init__(self, repo_productos=None, repo_movimientos=None):
        self.__productos = repo_productos or ProductoRepositorio()
        self.__movimientos = repo_movimientos or MovimientoRepositorio()

    def buscar(self, codigo):
        producto = self.__productos.obtener(codigo)
        if producto is None:
            raise ValueError(f"No existe un producto con código {codigo}.")
        return producto

    def listar(self):
        return self.__productos.listar()

    # ---------- HU01: ingresar producto ----------
    def agregar_producto(self, codigo, nombre, stock_inicial, stock_minimo, precio=0):
        if not codigo or not nombre:
            raise ValueError("El código y el nombre son obligatorios.")
        if self.__productos.existe(codigo):
            raise ValueError(f"Ya existe un producto con código {codigo}.")
        if stock_inicial < 0 or stock_minimo < 0:
            raise ValueError("El stock no puede ser negativo.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        producto = Producto(codigo, nombre, stock_inicial, stock_minimo, precio)
        self.__productos.guardar(producto)
        return producto

    # ---------- HU02 y HU05: entradas de stock ----------
    def registrar_alta(self, codigo, cantidad, usuario, detalle=""):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        producto = self.buscar(codigo)
        producto.stock += cantidad
        self.__productos.actualizar(producto)
        self.__movimientos.guardar(codigo, Movimiento(Movimiento.ALTA, cantidad, usuario, detalle))
        return producto

    # ---------- HU03: salidas de stock ----------
    def registrar_baja(self, codigo, cantidad, usuario, detalle=""):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        producto = self.buscar(codigo)
        if cantidad > producto.stock:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}.")
        producto.stock -= cantidad
        self.__productos.actualizar(producto)
        self.__movimientos.guardar(codigo, Movimiento(Movimiento.BAJA, cantidad, usuario, detalle))
        return producto

    # ---------- HU04: modificar producto ----------
    def modificar_producto(self, codigo, nombre=None, precio=None, stock_minimo=None):
        producto = self.buscar(codigo)
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
    def historial(self, codigo):
        self.buscar(codigo)   # valida que exista
        return self.__movimientos.listar_por_producto(codigo)

    # ---------- HU08: eliminar producto ----------
    def eliminar_producto(self, codigo):
        producto = self.buscar(codigo)
        self.__productos.eliminar(codigo)
        self.__movimientos.eliminar_por_producto(codigo)
        return producto
