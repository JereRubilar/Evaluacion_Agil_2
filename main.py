"""Punto de entrada del Sistema de Control de Inventario."""

from ejemplo import cargar_datos_ejemplo
from interfaz.menus import menu_principal
from repositorios import MovimientoRepositorio, ProductoRepositorio
from servicios import Inventario


def main():
    # Aquí se eligen los repositorios. Para usar MySQL más adelante,
    # se reemplazan por versiones que lean y escriban en la base de datos.
    inv = Inventario(ProductoRepositorio(), MovimientoRepositorio())
    cargar_datos_ejemplo(inv)
    menu_principal(inv)


if __name__ == "__main__":
    main()
