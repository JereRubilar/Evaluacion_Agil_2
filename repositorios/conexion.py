import sqlite3
import hashlib

DB_NAME = "inventario.db"

def encriptar_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

def inicializar_base_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        contraseña_hash TEXT NOT NULL,
        rol TEXT NOT NULL CHECK (rol IN ('Administrador', 'Supervisor', 'Reponedor'))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        stock INTEGER NOT NULL CHECK (stock >= 0),
        stock_minimo INTEGER NOT NULL CHECK (stock_minimo >= 0),
        precio REAL NOT NULL DEFAULT 0.00 CHECK (precio >= 0),
        id_categoria INTEGER,
        CONSTRAINT fk_producto_categoria
            FOREIGN KEY (id_categoria)
            REFERENCES categoria(id_categoria)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimiento (
        id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('ALTA', 'BAJA')),
        cantidad INTEGER NOT NULL CHECK (cantidad > 0),
        id_usuario INTEGER NOT NULL,
        detalle TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_movimiento_producto 
            FOREIGN KEY (id_producto) 
            REFERENCES producto(id_producto) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
        CONSTRAINT fk_movimiento_usuario
            FOREIGN KEY (id_usuario)
            REFERENCES usuario(id_usuario) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
    );
    """)

    password_cifrada = encriptar_password("1234")
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (nombre, contraseña_hash, rol)
        VALUES (?, ?, ?)
    """, ("admin", password_cifrada, "Administrador"))

    conexion.commit()
    conexion.close()