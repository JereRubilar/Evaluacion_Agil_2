"""Una función por cada opción del menú (una por historia de usuario)."""

from Evaluacion_Agil_2.interfaz.utilidades import mostrar_alerta, pedir_codigo, pedir_entero


def listar_productos(inv, rol):
    productos = inv.listar()
    if not productos:
        print("  No hay productos registrados.")
        return
    print()
    for p in productos:
        print("  " + str(p))


def agregar_producto(inv, rol):
    print("\n--- Ingresar producto (HU01) ---")
    codigo = pedir_codigo("Código: ")
    nombre = input("Nombre: ").strip()
    stock_inicial = pedir_entero("Stock inicial: ")
    stock_minimo = pedir_entero("Stock mínimo: ")
    precio = pedir_entero("Precio (Enter para 0): ", permitir_vacio=True) or 0
    p = inv.agregar_producto(codigo, nombre, stock_inicial, stock_minimo, precio)
    print(f"  Producto '{p.nombre}' ingresado correctamente.")
    mostrar_alerta(p)


def registrar_alta(inv, rol):
    print("\n--- Registrar entrada de stock (HU02) ---")
    codigo = pedir_codigo()
    cantidad = pedir_entero("Cantidad a ingresar: ")
    p = inv.registrar_alta(codigo, cantidad, rol)
    print(f"  Stock actualizado. '{p.nombre}' ahora tiene {p.stock} unidades.")


def registrar_llegada(inv, rol):
    print("\n--- Ingresar productos recién llegados (HU05) ---")
    codigo = pedir_codigo()
    cantidad = pedir_entero("Cantidad recibida: ")
    p = inv.registrar_alta(codigo, cantidad, rol, "llegada de mercadería")
    print(f"  Recepción registrada. '{p.nombre}' ahora tiene {p.stock} unidades.")


def registrar_baja(inv, rol):
    print("\n--- Registrar salida de stock (HU03) ---")
    codigo = pedir_codigo()
    cantidad = pedir_entero("Cantidad a retirar: ")
    motivo = input("Motivo (venta/consumo/otro): ").strip()
    p = inv.registrar_baja(codigo, cantidad, rol, motivo)
    print(f"  Salida registrada. '{p.nombre}' ahora tiene {p.stock} unidades.")
    mostrar_alerta(p)


def modificar_producto(inv, rol):
    print("\n--- Modificar producto (HU04) ---")
    codigo = pedir_codigo()
    p = inv.buscar(codigo)
    print("  Actual: " + str(p))
    print("  (Deje en blanco lo que no quiera cambiar)")
    nombre = input("Nuevo nombre: ").strip() or None
    precio = pedir_entero("Nuevo precio: ", permitir_vacio=True)
    stock_minimo = pedir_entero("Nuevo stock mínimo: ", permitir_vacio=True)
    p = inv.modificar_producto(codigo, nombre, precio, stock_minimo)
    print("  Producto actualizado: " + str(p))
    mostrar_alerta(p)


def ver_alertas(inv, rol):
    print("\n--- Productos en stock mínimo (HU06) ---")
    alertas = inv.productos_en_alerta()
    if not alertas:
        print("  Ningún producto está en stock mínimo.")
    for p in alertas:
        print("  ⚠ " + str(p))


def ver_historial(inv, rol):
    print("\n--- Historial de movimientos (HU07) ---")
    codigo = pedir_codigo()
    p = inv.buscar(codigo)
    movimientos = inv.historial(codigo)
    print(f"  Producto: {p.nombre} | Stock actual: {p.stock}")
    if not movimientos:
        print("  Sin movimientos registrados.")
    for m in movimientos:
        print("  " + str(m))


def eliminar_producto(inv, rol):
    print("\n--- Eliminar producto no vigente (HU08) ---")
    codigo = pedir_codigo()
    p = inv.buscar(codigo)
    confirma = input(f"¿Seguro que desea eliminar '{p.nombre}'? (s/n): ").strip().lower()
    if confirma == "s":
        inv.eliminar_producto(codigo)
        print("  Producto eliminado.")
    else:
        print("  Operación cancelada.")
