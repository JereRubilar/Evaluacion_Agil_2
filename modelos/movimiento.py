
from datetime import datetime


class Movimiento:
    ALTA = "ALTA"
    BAJA = "BAJA"

    def __init__(self, tipo, cantidad, usuario, detalle=""):
        self.tipo = tipo              
        self.cantidad = cantidad
        self.usuario = usuario        
        self.detalle = detalle
        self.fecha = datetime.now()

    def __str__(self):
        fecha = self.fecha.strftime("%d-%m-%Y %H:%M")
        signo = "+" if self.tipo == Movimiento.ALTA else "-"
        texto = f"[{fecha}] {self.tipo:<4} {signo}{self.cantidad:<5} por {self.usuario}"
        if self.detalle:
            texto += f" ({self.detalle})"
        return texto
