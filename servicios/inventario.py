from modelos import Movimiento, Producto, Categoria
from repositorios import MovimientoRepositorio, ProductoRepositorio, CategoriaRepositorio


class Inventario:
    def __init__(self, producto_repo, movimiento_repo, categoria_repo=None):
        self.__productos = producto_repo
        self.__movimientos = movimiento_repo
        self.__repo_categorias = categoria_repo if categoria_repo else CategoriaRepositorio()

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
        producto = self.buscar(id_producto)
        if not producto:
            raise ValueError(f"No existe el producto con ID {id_producto}.")
        if cantidad <= 0:
            raise ValueError("La cantidad a ingresar debe ser mayor a 0.")
        
        producto.stock += cantidad
        self.__productos.actualizar(producto)

        movimiento = Movimiento(
            id_producto=id_producto,
            tipo=Movimiento.ALTA,
            cantidad=cantidad,
            id_usuario=id_usuario,
            detalle=detalle
        )
        self.__movimientos.guardar(movimiento)
        return producto

    # ---------- HU03: salidas de stock ----------
    def registrar_baja(self, id_producto, cantidad, id_usuario, detalle=""):
        producto = self.buscar(id_producto)
        if not producto:
            raise ValueError(f"No existe el producto con ID {id_producto}.")
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser mayor a 0.")
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Stock actual: {producto.stock}, solicitado: {cantidad}.")
        
        producto.stock -= cantidad
        self.__productos.actualizar(producto)

        movimiento = Movimiento(
            id_producto=id_producto,
            tipo=Movimiento.BAJA,
            cantidad=cantidad,
            id_usuario=id_usuario,
            detalle=detalle
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

    # ---------- HU09: Categorías / Etiquetas ----------
    def crear_categoria(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoría es obligatorio.")
        categoria = Categoria(nombre=nombre.strip())
        return self.__repo_categorias.guardar(categoria)

    def listar_categorias(self):
        return self.__repo_categorias.listar()

    def asignar_categoria_a_producto(self, id_producto, id_categoria):
        producto = self.buscar(id_producto)
        if not producto:
            raise ValueError(f"No existe el producto con ID {id_producto}.")

        if id_categoria is not None:
            categoria = self.__repo_categorias.obtener(id_categoria)
            if not categoria:
                raise ValueError(f"La categoría con ID {id_categoria} no existe.")
        
        producto.id_categoria = id_categoria
        self.__productos.actualizar(producto)
        return producto

    def listar_productos_por_categoria(self, id_categoria):
        return [p for p in self.listar() if p.id_categoria == id_categoria]

# ---------- HU10: Resumen diario automático de ventas y gastos ----------
    def resumen_diario(self):
        from repositorios.conexion import obtener_conexion
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT m.tipo, m.cantidad, p.precio, m.detalle
            FROM movimiento m
            JOIN producto p ON m.id_producto = p.id_producto
            WHERE DATE(m.fecha) = DATE('now', 'localtime')
        """)
        rows = cursor.fetchall()
        conexion.close()

        total_ventas_monto = 0.0
        total_ventas_cantidad = 0
        total_compras_gastos_monto = 0.0
        total_compras_cantidad = 0
        detalle_movimientos = []

        for tipo, cantidad, precio, detalle in rows:
            subtotal = cantidad * precio
            if tipo == Movimiento.BAJA:
                total_ventas_cantidad += cantidad
                total_ventas_monto += subtotal
            elif tipo == Movimiento.ALTA:
                total_compras_cantidad += cantidad
                total_compras_gastos_monto += subtotal
            
            detalle_movimientos.append({
                "tipo": tipo,
                "cantidad": cantidad,
                "subtotal": subtotal,
                "detalle": detalle
            })

        return {
            "ventas": {
                "cantidad_unidades": total_ventas_cantidad,
                "monto_total": total_ventas_monto
            },
            "gastos_compras": {
                "cantidad_unidades": total_compras_cantidad,
                "monto_total": total_compras_gastos_monto
            },
            "operaciones_hoy": len(rows),
            "detalle": detalle_movimientos
        }

    def exportar_movimientos_csv(self, ruta_archivo):
        import csv
        movimientos = self.__movimientos.listar_con_detalles()
        
        try:
            with open(ruta_archivo, mode='w', newline='', encoding='utf-8-sig') as archivo:
                writer = csv.writer(archivo, delimiter=';') # Usamos punto y coma para mejor compatibilidad con Excel en español
                
                # Cabecera de la planilla
                writer.writerow(["ID Movimiento", "ID Producto", "Producto", "Tipo", "Cantidad", "ID Usuario", "Usuario", "Motivo / Detalle", "Fecha y Hora"])
                
                # Filas de datos
                for row in movimientos:
                    writer.writerow(row)
            return True
        except Exception as e:
            raise ValueError(f"Error al generar el archivo CSV: {e}")