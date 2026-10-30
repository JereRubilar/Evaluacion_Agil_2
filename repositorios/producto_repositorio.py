from modelos import Producto
from repositorios.conexion import obtener_conexion

class ProductoRepositorio:
    def guardar(self, producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO producto (nombre, stock, stock_minimo, precio) VALUES (?, ?, ?, ?)",
            (producto.nombre, producto.stock, producto.stock_minimo, producto.precio)
        )
        conexion.commit()
        producto.id_producto = cursor.lastrowid
        conexion.close()
        return producto

    def obtener(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre, stock, stock_minimo, precio FROM producto WHERE id_producto = ?", (id_producto,))
        row = cursor.fetchone()
        conexion.close()
        if row:
            return Producto(nombre=row[1], stock=row[2], stock_minimo=row[3], precio=row[4], id_producto=row[0])
        return None

    def existe(self, id_producto):
        return self.obtener(id_producto) is not None

    def listar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre, stock, stock_minimo, precio FROM producto")
        rows = cursor.fetchall()
        conexion.close()
        return [
            Producto(nombre=row[1], stock=row[2], stock_minimo=row[3], precio=row[4], id_producto=row[0])
            for row in rows
        ]

    def eliminar(self, id_producto):
        producto = self.obtener(id_producto)
        if producto:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM producto WHERE id_producto = ?", (id_producto,))
            conexion.commit()
            conexion.close()
            return producto
        return None

    def actualizar(self, producto):
        if not self.existe(producto.id_producto):
            raise ValueError(f"No existe un producto con ID {producto.id_producto}.")
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE producto SET nombre = ?, stock = ?, stock_minimo = ?, precio = ? WHERE id_producto = ?",
            (producto.nombre, producto.stock, producto.stock_minimo, producto.precio, producto.id_producto)
        )
        conexion.commit()
        conexion.close()