# Sistema de Control de Inventario (avance)

Programa de consola en Python para controlar el inventario de productos según historias de usuario.

## Ejecutar

```
python main.py
```

Pruebas:

```
python -m unittest
```

## Estructura

```
sistema-inventario/
├── main.py                  # Punto de entrada
├── modelos/                 # Clases de datos
│   ├── producto.py
│   └── movimiento.py
├── repositorios/            # Acceso a datos (encapsulado)
│   ├── producto_repositorio.py
│   └── movimiento_repositorio.py
├── servicios/               # Reglas de negocio (historias de usuario)
│   └── inventario.py
├── interfaz/                # Menús y pantallas de consola
│   ├── menus.py
│   ├── acciones.py
│   └── utilidades.py
├── datos/ejemplo.py         # Productos de prueba
└── tests/test_inventario.py
```

Flujo: `interfaz` → `servicios` → `repositorios` → datos.
La interfaz nunca toca los datos directamente, y el servicio no sabe cómo se guardan.

## Historias de usuario

| ID | Rol | Historia |
|----|-----|----------|
| HU01 | Administrador | Ingresar productos con nombre, código, stock inicial y stock mínimo |
| HU02 | Supervisor | Registrar entradas (altas) de stock |
| HU03 | Supervisor | Registrar salidas (bajas) de stock |
| HU04 | Administrador | Modificar datos de un producto (precio, nombre, stock mínimo) |
| HU05 | Reponedor | Ingresar productos recién llegados |
| HU06 | Administrador | Recibir alerta cuando un producto alcance su stock mínimo |
| HU07 | Supervisor | Consultar historial de altas y bajas de un producto |
| HU08 | Administrador | Eliminar productos que ya no estén vigentes |
| HU09–HU12 | — | Pendientes |
