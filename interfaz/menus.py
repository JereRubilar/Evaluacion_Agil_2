
from interfaz import acciones
from interfaz.utilidades import pedir_entero

MENUS = {
    "Administrador": [
        ("Ingresar producto", acciones.agregar_producto),
        ("Modificar producto", acciones.modificar_producto),
        ("Ver alertas de stock mínimo", acciones.ver_alertas),
        ("Eliminar producto no vigente", acciones.eliminar_producto),
        ("Listar productos", acciones.listar_productos),
    ],
    "Supervisor": [
        ("Registrar entrada (alta)", acciones.registrar_alta),
        ("Registrar salida (baja)", acciones.registrar_baja),
        ("Consultar historial de un producto", acciones.ver_historial),
        ("Listar productos", acciones.listar_productos),
    ],
    "Reponedor": [
        ("Ingresar productos recién llegados", acciones.registrar_llegada),
        ("Listar productos", acciones.listar_productos),
    ],
}


def menu_rol(inv, rol):
    opciones = MENUS[rol]
    alertas = inv.productos_en_alerta()
    if rol == "Administrador" and alertas:
        print(f"\n  ⚠ Hay {len(alertas)} producto(s) en stock mínimo.")
    while True:
        print(f"\n===== Menú {rol} =====")
        for i, (texto, _) in enumerate(opciones, 1):
            print(f"  {i}. {texto}")
        print("  0. Cambiar de usuario")
        opcion = pedir_entero("Opción: ")
        if opcion == 0:
            return
        if 1 <= opcion <= len(opciones):
            try:
                opciones[opcion - 1][1](inv, rol)
            except ValueError as e:
                print(f"  Error: {e}")
        else:
            print("  Opción no válida.")


def menu_principal(inv):
    roles = list(MENUS.keys())
    while True:
        print("\n===== SISTEMA DE INVENTARIO =====")
        for i, rol in enumerate(roles, 1):
            print(f"  {i}. {rol}")
        print("  0. Salir")
        opcion = pedir_entero("Ingrese como: ")
        if opcion == 0:
            print("Hasta luego.")
            break
        if 1 <= opcion <= len(roles):
            menu_rol(inv, roles[opcion - 1])
        else:
            print("  Opción no válida.")
