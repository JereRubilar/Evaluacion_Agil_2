import tkinter as tk
from tkinter import messagebox, ttk
from repositorios import (
    UsuarioRepositorio, 
    ProductoRepositorio, 
    MovimientoRepositorio, 
    CategoriaRepositorio
)
from servicios import Inventario

class AppInventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario - Pyme")
        self.root.geometry("1050x720")
        self.root.config(bg="#f0f0f0")

        self.inv = Inventario(ProductoRepositorio(), MovimientoRepositorio())
        self.repo_usuarios = UsuarioRepositorio()
        self.repo_categorias = CategoriaRepositorio()

        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()
        self.root.geometry("500x400")

        frame = tk.Frame(self.root, bg="white", padx=20, pady=20, relief="raised", borderwidth=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)

        tk.Label(frame, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(frame, text="Usuario:", bg="white", anchor="w").pack(fill="x")
        self.entry_usuario = tk.Entry(frame, font=("Arial", 12))
        self.entry_usuario.pack(fill="x", pady=5)

        tk.Label(frame, text="Contraseña:", bg="white", anchor="w").pack(fill="x")
        self.entry_password = tk.Entry(frame, font=("Arial", 12), show="*")
        self.entry_password.pack(fill="x", pady=5)

        btn_login = tk.Button(
            frame, 
            text="Ingresar", 
            bg="#007ACC", 
            fg="white", 
            font=("Arial", 11, "bold"), 
            command=self.verificar_login
        )
        btn_login.pack(fill="x", pady=20)

    def verificar_login(self):
        nombre = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not nombre or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        usuario = self.repo_usuarios.obtener_por_nombre(nombre)
        if usuario and usuario.contraseña_hash == password:
            self.entry_usuario.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.mostrar_panel_principal(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def mostrar_panel_principal(self, usuario):
        self.usuario_actual = usuario
        self.limpiar_ventana()
        self.root.geometry("1050x720")

        # --- Barra Superior ---
        top_bar = tk.Frame(self.root, bg="#007ACC", height=50)
        top_bar.pack(fill="x")

        tk.Label(
            top_bar, 
            text=f"👤 Usuario: {usuario.nombre} | Rol: {usuario.rol}", 
            fg="white", 
            bg="#007ACC", 
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=15, pady=10)
        
        btn_salir = tk.Button(
            top_bar, 
            text="Cerrar Sesión", 
            bg="#ff4d4d", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.mostrar_login
        )
        btn_salir.pack(side="right", padx=15, pady=10)

        # --- Contenedor Principal ---
        content_frame = tk.Frame(self.root, padx=20, pady=15, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True)

        tk.Label(content_frame, text="Panel de Control y Stock", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor="w", pady=2)

        # --- HU-10: Tarjeta de Resumen Diario Automático ---
        self.resumen_frame = tk.LabelFrame(
            content_frame, 
            text="📊 Resumen Diario Automático (Hoy)", 
            font=("Arial", 11, "bold"), 
            bg="#ffffff", 
            fg="#333333",
            padx=15, 
            pady=10,
            relief="groove",
            borderwidth=2
        )
        self.resumen_frame.pack(fill="x", pady=8)

        # Labels internos del resumen
        self.lbl_ventas = tk.Label(self.resumen_frame, text="", font=("Arial", 10, "bold"), bg="#ffffff", fg="#2E7D32")
        self.lbl_ventas.pack(anchor="w", pady=2)

        self.lbl_gastos = tk.Label(self.resumen_frame, text="", font=("Arial", 10, "bold"), bg="#ffffff", fg="#C62828")
        self.lbl_gastos.pack(anchor="w", pady=2)

        self.lbl_ops = tk.Label(self.resumen_frame, text="", font=("Arial", 9, "italic"), bg="#ffffff", fg="#666666")
        self.lbl_ops.pack(anchor="w", pady=2)

        # --- Tabla de Productos (Treeview) ---
        table_frame = tk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, pady=5)

        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side="right", fill="y")

        columns = ("id", "nombre", "categoria", "stock", "stock_minimo", "precio")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre del Producto")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("stock", text="Stock Actual")
        self.tree.heading("stock_minimo", text="Stock Mínimo")
        self.tree.heading("precio", text="Precio ($)")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=220, anchor="w")
        self.tree.column("categoria", width=140, anchor="w")
        self.tree.column("stock", width=90, anchor="center")
        self.tree.column("stock_minimo", width=90, anchor="center")
        self.tree.column("precio", width=100, anchor="e")

        self.tree.tag_configure("alerta", background="#ffcccc")
        self.tree.pack(fill="both", expand=True)

        # --- Botonera de Acciones Inferior ---
        actions_frame = tk.Frame(content_frame, bg="#f0f0f0")
        actions_frame.pack(fill="x", pady=10)

        btn_actualizar = tk.Button(
            actions_frame, 
            text="🔄 Actualizar", 
            bg="#757575", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.actualizar_vista_completa
        )
        btn_actualizar.pack(side="left", padx=4)

        btn_alertas = tk.Button(
            actions_frame, 
            text="⚠️ Alertas Stock", 
            bg="#D35400", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.abrir_ventana_alertas
        )
        btn_alertas.pack(side="left", padx=4)

        btn_historial = tk.Button(
            actions_frame, 
            text="📋 Ver Historial", 
            bg="#2980B9", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=self.abrir_ventana_historial
        )
        btn_historial.pack(side="left", padx=4)

        btn_alta = tk.Button(
            actions_frame, 
            text="⬆ Entrada", 
            bg="#2E7D32", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=lambda: self.abrir_ventana_movimiento("ALTA")
        )
        btn_alta.pack(side="left", padx=4)

        btn_baja = tk.Button(
            actions_frame, 
            text="⬇ Salida", 
            bg="#C62828", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            command=lambda: self.abrir_ventana_movimiento("BAJA")
        )
        btn_baja.pack(side="left", padx=4)

        if usuario.rol == "Administrador":
            btn_agregar = tk.Button(
                actions_frame, 
                text="➕ Nuevo", 
                bg="#007ACC", 
                fg="white", 
                font=("Arial", 9, "bold"), 
                command=self.abrir_ventana_agregar_producto
            )
            btn_agregar.pack(side="left", padx=4)

            btn_modificar = tk.Button(
                actions_frame, 
                text="✏ Modificar", 
                bg="#FF9800", 
                fg="white", 
                font=("Arial", 9, "bold"), 
                command=self.abrir_ventana_modificar_producto
            )
            btn_modificar.pack(side="left", padx=4)

            btn_eliminar = tk.Button(
                actions_frame, 
                text="🗑 Eliminar", 
                bg="#D32F2F", 
                fg="white", 
                font=("Arial", 9, "bold"), 
                command=self.ejecutar_eliminar_producto
            )
            btn_eliminar.pack(side="left", padx=4)

        # Cargar datos iniciales (tabla + resumen)
        self.actualizar_vista_completa()

    def actualizar_vista_completa(self):
        """Refresca tanto la tabla de productos como la tarjeta de resumen diario."""
        self.cargar_productos_tabla()
        self.actualizar_resumen_diario()

    def cargar_productos_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        productos = self.inv.listar()
        for p in productos:
            cat_nombre = p.nombre_categoria if hasattr(p, 'nombre_categoria') and p.nombre_categoria else "Sin Categoría"
            tag = "alerta" if p.en_stock_minimo() else ""
            
            self.tree.insert("", "end", values=(
                p.id_producto,
                p.nombre,
                cat_nombre,
                p.stock,
                p.stock_minimo,
                f"${p.precio:,.2f}"
            ), tags=(tag,))

    def actualizar_resumen_diario(self):
        """Consulta el servicio y actualiza los textos de la tarjeta de resumen diario (HU-10)."""
        resumen = self.inv.resumen_diario()
        
        ventas_monto = resumen["ventas"]["monto_total"]
        ventas_cant = resumen["ventas"]["cantidad_unidades"]
        
        gastos_monto = resumen["gastos_compras"]["monto_total"]
        gastos_cant = resumen["gastos_compras"]["monto_unidades"] if "monto_unidades" in resumen["gastos_compras"] else resumen["gastos_compras"]["cantidad_unidades"]
        
        ops_hoy = resumen["operaciones_hoy"]

        self.lbl_ventas.config(text=f"🟢 Ventas del Día: ${ventas_monto:,.2f}  (Unidades vendidas: {ventas_cant})")
        self.lbl_gastos.config(text=f"🔴 Compras / Gastos del Día: ${gastos_monto:,.2f}  (Unidades ingresadas: {gastos_cant})")
        self.lbl_ops.config(text=f"📋 Total de operaciones registradas hoy: {ops_hoy}")

    def obtener_id_producto_seleccionado(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            return int(values[0])
        return None

    # --- VENTANA EMERGENTE DE ALERTAS DE STOCK ---
    def abrir_ventana_alertas(self):
        alertas = self.inv.productos_en_alerta()
        
        win = tk.Toplevel(self.root)
        win.title("Productos en Stock Mínimo (Alertas)")
        win.geometry("550x350")
        win.grab_set()

        tk.Label(win, text="⚠️ Productos que requieren reposición", font=("Arial", 13, "bold"), fg="#D35400").pack(pady=10)

        if not alertas:
            tk.Label(win, text="¡Excelente! Ningún producto está en stock mínimo.", font=("Arial", 11), fg="green").pack(pady=40)
            return

        table_frame = tk.Frame(win, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "nombre", "stock", "minimo")
        tree_alt = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree_alt.heading("id", text="ID")
        tree_alt.heading("nombre", text="Producto")
        tree_alt.heading("stock", text="Stock Actual")
        tree_alt.heading("minimo", text="Stock Mínimo")

        tree_alt.column("id", width=50, anchor="center")
        tree_alt.column("nombre", width=220, anchor="w")
        tree_alt.column("stock", width=100, anchor="center")
        tree_alt.column("minimo", width=100, anchor="center")

        tree_alt.pack(fill="both", expand=True)

        for p in alertas:
            tree_alt.insert("", "end", values=(p.id_producto, p.nombre, p.stock, p.stock_minimo))

    # --- VENTANA EMERGENTE DE HISTORIAL DE MOVIMIENTOS ---
    def abrir_ventana_historial(self):
        id_sel = self.obtener_id_producto_seleccionado()
        if not id_sel:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la tabla para ver su historial.")
            return

        try:
            producto = self.inv.buscar(id_sel)
            movimientos = self.inv.historial(id_sel)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        win = tk.Toplevel(self.root)
        win.title(f"Historial - {producto.nombre} (ID #{producto.id_producto})")
        win.geometry("650x400")
        win.grab_set()

        tk.Label(win, text=f"Historial de Movimientos: {producto.nombre}", font=("Arial", 13, "bold")).pack(pady=10)
        tk.Label(win, text=f"Stock Actual: {producto.stock} unidades", font=("Arial", 10, "italic")).pack(anchor="w", padx=20)

        table_frame = tk.Frame(win, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("id_mov", "tipo", "cantidad", "usuario", "detalle", "fecha")
        tree_hist = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree_hist.heading("id_mov", text="#Mov")
        tree_hist.heading("tipo", text="Tipo")
        tree_hist.heading("cantidad", text="Cant.")
        tree_hist.heading("usuario", text="Usuario ID")
        tree_hist.heading("detalle", text="Detalle / Motivo")
        tree_hist.heading("fecha", text="Fecha y Hora")

        tree_hist.column("id_mov", width=50, anchor="center")
        tree_hist.column("tipo", width=70, anchor="center")
        tree_hist.column("cantidad", width=60, anchor="center")
        tree_hist.column("usuario", width=80, anchor="center")
        tree_hist.column("detalle", width=160, anchor="w")
        tree_hist.column("fecha", width=130, anchor="center")

        tree_hist.pack(fill="both", expand=True)

        if not movimientos:
            tk.Label(win, text="No hay movimientos registrados para este producto.", fg="gray").pack(pady=10)

        for m in movimientos:
            tree_hist.insert("", "end", values=(
                m.id_movimiento,
                m.tipo,
                m.cantidad,
                m.id_usuario,
                m.detalle or "-",
                m.fecha
            ))

    # --- VENTANA EMERGENTE: AGREGAR PRODUCTO ---
    def abrir_ventana_agregar_producto(self):
        win = tk.Toplevel(self.root)
        win.title("Ingresar Nuevo Producto")
        win.geometry("380x420")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="Ingresar Producto", font=("Arial", 14, "bold")).pack(pady=10)

        frame_form = tk.Frame(win, padx=20, pady=10)
        frame_form.pack(fill="both", expand=True)

        tk.Label(frame_form, text="Nombre:", anchor="w").pack(fill="x")
        entry_nombre = tk.Entry(frame_form, font=("Arial", 10))
        entry_nombre.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Stock Inicial:", anchor="w").pack(fill="x")
        entry_stock = tk.Entry(frame_form, font=("Arial", 10))
        entry_stock.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Stock Mínimo:", anchor="w").pack(fill="x")
        entry_stock_min = tk.Entry(frame_form, font=("Arial", 10))
        entry_stock_min.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Precio ($):", anchor="w").pack(fill="x")
        entry_precio = tk.Entry(frame_form, font=("Arial", 10))
        entry_precio.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Categoría:", anchor="w").pack(fill="x")
        categorias = self.repo_categorias.listar()
        cat_dict = {c.nombre: c.id_categoria for c in categorias}
        cat_options = ["Sin Categoría"] + list(cat_dict.keys())

        combo_categoria = ttk.Combobox(frame_form, values=cat_options, state="readonly")
        combo_categoria.set("Sin Categoría")
        combo_categoria.pack(fill="x", pady=4)

        def guardar_producto():
            nombre = entry_nombre.get().strip()
            try:
                stock_inicial = int(entry_stock.get().strip())
                stock_minimo = int(entry_stock_min.get().strip())
                precio = float(entry_precio.get().strip()) if entry_precio.get().strip() else 0.0
            except ValueError:
                messagebox.showerror("Error", "Stock y Stock Mínimo deben ser enteros, y Precio un decimal.")
                return

            cat_seleccionada = combo_categoria.get()
            id_cat = cat_dict.get(cat_seleccionada) if cat_seleccionada in cat_dict else None

            try:
                p = self.inv.agregar_producto(
                    nombre=nombre, 
                    stock_inicial=stock_inicial, 
                    stock_minimo=stock_minimo, 
                    precio=precio
                )
                if id_cat:
                    self.inv.asignar_categoria_a_producto(p.id_producto, id_cat)

                messagebox.showinfo("Éxito", f"Producto '{p.nombre}' creado correctamente.")
                self.actualizar_vista_completa()
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        btn_guardar = tk.Button(
            frame_form, 
            text="Guardar Producto", 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            command=guardar_producto
        )
        btn_guardar.pack(fill="x", pady=15)

    # --- VENTANA EMERGENTE: MODIFICAR PRODUCTO ---
    def abrir_ventana_modificar_producto(self):
        id_sel = self.obtener_id_producto_seleccionado()
        if not id_sel:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la tabla para modificar.")
            return

        producto = self.inv.buscar(id_sel)

        win = tk.Toplevel(self.root)
        win.title(f"Modificar Producto ID #{producto.id_producto}")
        win.geometry("380x380")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text=f"Modificar ID #{producto.id_producto}", font=("Arial", 13, "bold")).pack(pady=10)

        frame_form = tk.Frame(win, padx=20, pady=10)
        frame_form.pack(fill="both", expand=True)

        tk.Label(frame_form, text="Nombre:", anchor="w").pack(fill="x")
        entry_nombre = tk.Entry(frame_form, font=("Arial", 10))
        entry_nombre.insert(0, producto.nombre)
        entry_nombre.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Stock Mínimo:", anchor="w").pack(fill="x")
        entry_stock_min = tk.Entry(frame_form, font=("Arial", 10))
        entry_stock_min.insert(0, str(producto.stock_minimo))
        entry_stock_min.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Precio ($):", anchor="w").pack(fill="x")
        entry_precio = tk.Entry(frame_form, font=("Arial", 10))
        entry_precio.insert(0, str(producto.precio))
        entry_precio.pack(fill="x", pady=4)

        tk.Label(frame_form, text="Categoría:", anchor="w").pack(fill="x")
        categorias = self.repo_categorias.listar()
        cat_dict = {c.nombre: c.id_categoria for c in categorias}
        cat_options = ["Sin Categoría"] + list(cat_dict.keys())

        combo_categoria = ttk.Combobox(frame_form, values=cat_options, state="readonly")
        cat_actual = producto.nombre_categoria if hasattr(producto, 'nombre_categoria') and producto.nombre_categoria else "Sin Categoría"
        combo_categoria.set(cat_actual)
        combo_categoria.pack(fill="x", pady=4)

        def guardar_modificacion():
            nombre = entry_nombre.get().strip()
            try:
                stock_minimo = int(entry_stock_min.get().strip())
                precio = float(entry_precio.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Stock Mínimo debe ser un entero y Precio un decimal.")
                return

            cat_seleccionada = combo_categoria.get()
            id_cat = cat_dict.get(cat_seleccionada) if cat_seleccionada in cat_dict else None

            try:
                self.inv.modificar_producto(
                    id_producto=producto.id_producto,
                    nombre=nombre,
                    precio=precio,
                    stock_minimo=stock_minimo
                )
                self.inv.asignar_categoria_a_producto(producto.id_producto, id_cat)

                messagebox.showinfo("Éxito", f"Producto '{nombre}' actualizado correctamente.")
                self.actualizar_vista_completa()
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        btn_guardar = tk.Button(
            frame_form, 
            text="Guardar Cambios", 
            bg="#FF9800", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            command=guardar_modificacion
        )
        btn_guardar.pack(fill="x", pady=15)

    # --- ELIMINAR PRODUCTO ---
    def ejecutar_eliminar_producto(self):
        id_sel = self.obtener_id_producto_seleccionado()
        if not id_sel:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la tabla para eliminar.")
            return

        producto = self.inv.buscar(id_sel)
        
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Estás seguro de que deseas eliminar permanentemente el producto '{producto.nombre}' (ID #{producto.id_producto})?\n\nEsta acción no se puede deshacer."
        )

        if confirmar:
            try:
                self.inv.eliminar_producto(producto.id_producto)
                messagebox.showinfo("Eliminado", f"El producto '{producto.nombre}' ha sido eliminado.")
                self.actualizar_vista_completa()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # --- VENTANA EMERGENTE: ENTRADAS Y SALIDAS DE STOCK ---
    def abrir_ventana_movimiento(self, tipo):
        titulo = "Registrar Entrada (Alta)" if tipo == "ALTA" else "Registrar Salida (Baja)"
        color_btn = "#2E7D32" if tipo == "ALTA" else "#C62828"

        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry("360x350")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text=titulo, font=("Arial", 13, "bold")).pack(pady=10)

        frame_form = tk.Frame(win, padx=20, pady=10)
        frame_form.pack(fill="both", expand=True)

        tk.Label(frame_form, text="ID del Producto:", anchor="w").pack(fill="x")
        entry_id = tk.Entry(frame_form, font=("Arial", 10))
        entry_id.pack(fill="x", pady=4)

        id_sel = self.obtener_id_producto_seleccionado()
        if id_sel:
            entry_id.insert(0, str(id_sel))

        tk.Label(frame_form, text="Cantidad:", anchor="w").pack(fill="x")
        entry_cantidad = tk.Entry(frame_form, font=("Arial", 10))
        entry_cantidad.pack(fill="x", pady=4)

        label_detalle = "Motivo / Detalle (Opcional):" if tipo == "ALTA" else "Motivo (Venta / Consumo / Otro):"
        tk.Label(frame_form, text=label_detalle, anchor="w").pack(fill="x")
        entry_detalle = tk.Entry(frame_form, font=("Arial", 10))
        entry_detalle.pack(fill="x", pady=4)

        def procesar_movimiento():
            try:
                id_producto = int(entry_id.get().strip())
                cantidad = int(entry_cantidad.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID y la cantidad deben ser números enteros válidos.")
                return

            detalle = entry_detalle.get().strip()

            try:
                if tipo == "ALTA":
                    p = self.inv.registrar_alta(
                        id_producto=id_producto, 
                        cantidad=cantidad, 
                        id_usuario=self.usuario_actual.id_usuario, 
                        detalle=detalle
                    )
                    messagebox.showinfo("Stock Actualizado", f"Entrada registrada. '{p.nombre}' ahora tiene {p.stock} unidades.")
                else:
                    p = self.inv.registrar_baja(
                        id_producto=id_producto, 
                        cantidad=cantidad, 
                        id_usuario=self.usuario_actual.id_usuario, 
                        detalle=detalle
                    )
                    alerta = f"\n⚠ ALERTA: Stock en mínimo ({p.stock})" if p.en_stock_minimo() else ""
                    messagebox.showinfo("Stock Actualizado", f"Salida registrada. '{p.nombre}' ahora tiene {p.stock} unidades.{alerta}")

                self.actualizar_vista_completa()
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Error en operación", str(e))

        btn_confirmar = tk.Button(
            frame_form, 
            text="Confirmar Operación", 
            bg=color_btn, 
            fg="white", 
            font=("Arial", 10, "bold"), 
            command=procesar_movimiento
        )
        btn_confirmar.pack(fill="x", pady=15)