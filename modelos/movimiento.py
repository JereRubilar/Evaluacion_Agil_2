from datetime import datetime


class Movimiento:
    ALTA = "ALTA"
    BAJA = "BAJA"

    def __init__(self, id_producto, tipo, cantidad, id_usuario, fecha=None, id_movimiento=None):
        self.id_movimiento = id_movimiento
        self.id_producto = id_producto
        self.tipo = tipo
        self.cantidad = cantidad
        self.id_usuario = id_usuario
        self.fecha = fecha or datetime.now()

    def __str__(self):
        fecha_str = (
            self.fecha.strftime("%d-%m-%Y %H:%M") 
            if isinstance(self.fecha, datetime) 
            else str(self.fecha)
        )
        signo = "+" if self.tipo == Movimiento.ALTA else "-"
        return (f"[{fecha_str}] Mov #{self.id_movimiento or 'N/A'} | Prod ID: {self.id_producto} | "
                f"{self.tipo:<4} {signo}{self.cantidad:<5} | Usuario ID: {self.id_usuario}")