"""Funciones de apoyo para la consola."""


def pedir_entero(mensaje, permitir_vacio=False):
    while True:
        valor = input(mensaje).strip()
        if permitir_vacio and valor == "":
            return None
        try:
            return int(valor)
        except ValueError:
            print("  Debe ingresar un número entero.")


def pedir_codigo(mensaje="Código del producto: "):
    return input(mensaje).strip().upper()


def mostrar_alerta(producto):
    """HU06: alerta inmediata al alcanzar el stock mínimo."""
    if producto.en_stock_minimo():
        print(f"\n  ⚠ ALERTA: '{producto.nombre}' alcanzó su stock mínimo "
              f"(stock actual: {producto.stock}, mínimo: {producto.stock_minimo}). "
              f"Se recomienda reponer.")
