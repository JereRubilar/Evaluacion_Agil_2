from modelos.categoria import Categoria
from repositorios.conexion import obtener_conexion

class CategoriaRepositorio:
    def guardar(self, categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO categoria (nombre) VALUES (?)",
            (categoria.nombre,)
        )
        conexion.commit()
        categoria.id_categoria = cursor.lastrowid
        conexion.close()
        return categoria

    def obtener(self, id_categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria WHERE id_categoria = ?", (id_categoria,))
        row = cursor.fetchone()
        conexion.close()
        if row:
            return Categoria(nombre=row[1], id_categoria=row[0])
        return None

    def listar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria ORDER BY nombre ASC")
        rows = cursor.fetchall()
        conexion.close()
        return [Categoria(nombre=row[1], id_categoria=row[0]) for row in rows]

    def eliminar(self, id_categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categoria WHERE id_categoria = ?", (id_categoria,))
        conexion.commit()
        conexion.close()