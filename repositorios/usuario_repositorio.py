from modelos.usuario import Usuario
from repositorios.conexion import obtener_conexion

class UsuarioRepositorio:
    def guardar(self, usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, contraseña_hash, rol) VALUES (?, ?, ?)",
            (usuario.nombre, usuario.contraseña_hash, usuario.rol)
        )
        conexion.commit()
        usuario.id_usuario = cursor.lastrowid
        conexion.close()
        return usuario

    def obtener_por_nombre(self, nombre):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, contraseña_hash, rol FROM usuario WHERE nombre = ?", 
            (nombre,)
        )
        row = cursor.fetchone()
        conexion.close()
        if row:
            return Usuario(id_usuario=row[0], nombre=row[1], contraseña_hash=row[2], rol=row[3])
        return None

    def listar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, contraseña_hash, rol FROM usuario")
        rows = cursor.fetchall()
        conexion.close()
        return [Usuario(id_usuario=row[0], nombre=row[1], contraseña_hash=row[2], rol=row[3]) for row in rows]