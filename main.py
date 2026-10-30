
from interfaz.menus import menu_principal
from repositorios import MovimientoRepositorio, ProductoRepositorio
from servicios import Inventario


def main():
    inv = Inventario(ProductoRepositorio(), MovimientoRepositorio())


if __name__ == "__main__":
    main()