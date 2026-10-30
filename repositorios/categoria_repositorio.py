from modelos.categoria import Categoria
from repositorios.conexion import obtener_conexion

class CategoriaRepositorio:
    def guardar(self, categoria):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO categoria (nombre) VALUES (?)", (categoria.nombre,))
        conexion.commit()
        categoria.id_categoria = cursor.lastrowid
        conexion.close()
        return categoria

    def listar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria")
        rows = cursor.fetchall()
        conexion.close()
        return [Categoria(id_categoria=row[0], nombre=row[1]) for row in rows]

    def obtener(self, id_categoria):
        """Busca y retorna una categoría por su ID, o None si no existe."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria WHERE id_categoria = ?", (id_categoria,))
        row = cursor.fetchone()
        conexion.close()
        
        if row:
            return Categoria(id_categoria=row[0], nombre=row[1])
        return None