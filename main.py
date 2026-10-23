"""Punto de entrada del Sistema de Control de Inventario."""

from Evaluacion_Agil_2.ejemplo import cargar_datos_ejemplo
from Evaluacion_Agil_2.interfaz.menus import menu_principal
from Evaluacion_Agil_2.repositorios import MovimientoRepositorio, ProductoRepositorio
from Evaluacion_Agil_2.servicios import Inventario


def main():
    # Aquí se eligen los repositorios. Para usar MySQL más adelante,
    # se reemplazan por versiones que lean y escriban en la base de datos.
    inv = Inventario(ProductoRepositorio(), MovimientoRepositorio())
    cargar_datos_ejemplo(inv)
    menu_principal(inv)


if __name__ == "__main__":
    main()
