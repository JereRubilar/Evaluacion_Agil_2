from modelos import Movimiento
from repositorios.conexion import obtener_conexion

class MovimientoRepositorio:
    def guardar(self, movimiento):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO movimiento (id_producto, tipo, cantidad, id_usuario) VALUES (?, ?, ?, ?)",
            (movimiento.id_producto, movimiento.tipo, movimiento.cantidad, movimiento.id_usuario)
        )
        conexion.commit()
        movimiento.id_movimiento = cursor.lastrowid
        conexion.close()
        return movimiento

    def listar_por_producto(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_movimiento, id_producto, tipo, cantidad, id_usuario, fecha FROM movimiento WHERE id_producto = ?",
            (id_producto,)
        )
        rows = cursor.fetchall()
        conexion.close()
        return [
            Movimiento(
                id_producto=row[1],
                tipo=row[2],
                cantidad=row[3],
                id_usuario=row[4],
                fecha=row[5],
                id_movimiento=row[0]
            )
            for row in rows
        ]

    def eliminar_por_producto(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM movimiento WHERE id_producto = ?", (id_producto,))
        conexion.commit()
        conexion.close()