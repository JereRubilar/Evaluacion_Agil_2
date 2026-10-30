class Usuario:
    def __init__(self, nombre, contraseña_hash, rol, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contraseña_hash = contraseña_hash
        self.rol = rol

    def __str__(self):
        return f"[{self.id_usuario or 'N/A'}] {self.nombre} ({self.rol})"