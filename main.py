import tkinter as tk
from repositorios import inicializar_base_datos
from interfaz.app_gui import AppInventario

def main():
    inicializar_base_datos()

    root = tk.Tk()
    app = AppInventario(root)
    root.mainloop()

if __name__ == "__main__":
    main()