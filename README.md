# Sistema de Inventario PyME (Escritorio)

Aplicación de escritorio desarrollada en **Python** y **Tkinter** con persistencia en **SQLite**, diseñada específicamente para PyMEs que necesitan un control ágil, seguro y centralizado de su stock, entradas, salidas y reportes financieros.

---

## Características Principales

El sistema opera bajo un esquema modular y por roles (Administrador, Supervisor y Reponedor):

* **Autenticación y Seguridad por Roles:** Control de acceso cifrado (SHA-256) con permisos diferenciados por perfil de usuario.
* **Gestión de Productos (CRUD):** Alta, modificación, listado y baja de productos con control de stock mínimo y precios.
* **Gestión de Categorías:** Organización jerárquica de los productos por categorías personalizadas.
* **Control de Stock (Entradas y Salidas):** Registro de altas y bajas de inventario especificando motivos o detalles de la operación (ventas, compras, mermas).
* **Alertas de Stock Mínimo:** Monitoreo en tiempo real de productos que requieren reposición inmediata.
* **Historial de Movimientos:** Trazabilidad completa por producto con registro de fecha, tipo de movimiento, usuario responsable y motivo.
* **Resumen Diario Automático (Exclusivo Admin):** Tarjeta interactiva en el panel principal con el balance del día (ventas, compras y total de operaciones).
* **Exportación de Planillas:** Generación de reportes detallados en formato CSV compatibles con Excel, Google Sheets y LibreOffice.

---

## 🛠️ Tecnologías y Librerías Utilizadas

Este proyecto se ha desarrollado **sin dependencias externas pesadas**, garantizando un rendimiento óptimo, bajo consumo de recursos y una integración limpia para su posterior empaquetado (`.exe` / binario):

* **Python 3.x** (LENGUAJE PRINCIPAL)
* **Tkinter / TTK** (Interfaz Gráfica de Escritorio nativa)
* **SQLite3** (Base de datos relacional integrada y local)
* **Hashlib** (Cifrado de credenciales de usuario con SHA-256)
* **CSV** (Módulo estándar para exportación de planillas compatibles con Excel)

---

## 📂 Estructura del Proyecto

```text
Evaluacion_Agil_2/
│
├── interfaz/         # Vistas y componentes gráficos en Tkinter (app_gui.py)
├── modelos/          # Clases de dominio (Producto, Categoria, Usuario, Movimiento)
├── repositorios/     # Capa de persistencia y conexión a SQLite (DAO)
├── servicios/        # Lógica de negocio e inventario (inventario.py)
├── inventario.db     # Base de datos local SQLite (se autogenera)
└── main.py           # Punto de entrada de la aplicación
