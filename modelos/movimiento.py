"""Modelo Movimiento: una alta o baja de stock (trazabilidad, HU07)."""

from datetime import datetime


class Movimiento:
    ALTA = "ALTA"
    BAJA = "BAJA"

    def __init__(self, tipo, cantidad, usuario, detalle=""):
        self.tipo = tipo              # Movimiento.ALTA o Movimiento.BAJA
        self.cantidad = cantidad
        self.usuario = usuario        # rol que hizo el movimiento
        self.detalle = detalle
        self.fecha = datetime.now()

    def __str__(self):
        fecha = self.fecha.strftime("%d-%m-%Y %H:%M")
        signo = "+" if self.tipo == Movimiento.ALTA else "-"
        texto = f"[{fecha}] {self.tipo:<4} {signo}{self.cantidad:<5} por {self.usuario}"
        if self.detalle:
            texto += f" ({self.detalle})"
        return texto
