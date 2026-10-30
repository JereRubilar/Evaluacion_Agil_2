from modelos.movimiento import Movimiento
from repositorios.conexion import obtener_conexion

class MovimientoRepositorio:
    def guardar(self, movimiento):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """INSERT INTO movimiento (id_producto, tipo, cantidad, id_usuario, detalle) 
               VALUES (?, ?, ?, ?, ?)""",
            (
                movimiento.id_producto, 
                movimiento.tipo, 
                movimiento.cantidad, 
                movimiento.id_usuario, 
                movimiento.detalle
            )
        )
        conexion.commit()
        movimiento.id_movimiento = cursor.lastrowid
        conexion.close()
        return movimiento

    def listar_por_producto(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """SELECT id_movimiento, id_producto, tipo, cantidad, id_usuario, detalle, fecha 
               FROM movimiento 
               WHERE id_producto = ? 
               ORDER BY fecha DESC""",
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
                detalle=row[5],
                fecha=row[6],
                id_movimiento=row[0]
            )
            for row in rows
        ]