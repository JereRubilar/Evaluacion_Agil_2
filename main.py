from repositorios import inicializar_base_datos, ProductoRepositorio, MovimientoRepositorio, UsuarioRepositorio
from servicios import Inventario

def main():
    inicializar_base_datos()

    repo_productos = ProductoRepositorio()
    repo_movimientos = MovimientoRepositorio()
    inv = Inventario(repo_productos, repo_movimientos)

    print("¡Sistema de Inventario iniciado correctamente con SQLite!")
    print(f"Productos actuales en la BD: {len(inv.listar())}")

if __name__ == "__main__":
    main()