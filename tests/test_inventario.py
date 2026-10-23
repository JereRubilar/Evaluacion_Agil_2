"""Pruebas de las historias de usuario. Ejecutar con: python -m unittest"""

import unittest

from repositorios import MovimientoRepositorio, ProductoRepositorio
from servicios import Inventario


class TestInventario(unittest.TestCase):
    def setUp(self):
        self.inv = Inventario(ProductoRepositorio(), MovimientoRepositorio())
        self.inv.agregar_producto("P001", "Arroz", 20, 5, 1000)

    def test_hu01_agregar_producto(self):
        self.assertEqual(self.inv.buscar("P001").nombre, "Arroz")

    def test_hu01_codigo_duplicado(self):
        with self.assertRaises(ValueError):
            self.inv.agregar_producto("P001", "Otro", 1, 1)

    def test_hu02_alta(self):
        self.inv.registrar_alta("P001", 10, "Supervisor")
        self.assertEqual(self.inv.buscar("P001").stock, 30)

    def test_hu03_baja(self):
        self.inv.registrar_baja("P001", 5, "Supervisor")
        self.assertEqual(self.inv.buscar("P001").stock, 15)

    def test_hu03_baja_sin_stock(self):
        with self.assertRaises(ValueError):
            self.inv.registrar_baja("P001", 100, "Supervisor")

    def test_hu04_modificar(self):
        self.inv.modificar_producto("P001", nombre="Arroz grado 1", precio=1200)
        p = self.inv.buscar("P001")
        self.assertEqual((p.nombre, p.precio), ("Arroz grado 1", 1200))

    def test_hu05_llegada(self):
        self.inv.registrar_alta("P001", 7, "Reponedor", "llegada de mercadería")
        self.assertEqual(self.inv.buscar("P001").stock, 27)

    def test_hu06_alerta(self):
        self.inv.registrar_baja("P001", 15, "Supervisor")
        self.assertIn(self.inv.buscar("P001"), self.inv.productos_en_alerta())

    def test_hu07_historial(self):
        self.inv.registrar_alta("P001", 3, "Supervisor")
        self.inv.registrar_baja("P001", 2, "Supervisor")
        self.assertEqual([m.tipo for m in self.inv.historial("P001")], ["ALTA", "BAJA"])

    def test_hu08_eliminar(self):
        self.inv.eliminar_producto("P001")
        with self.assertRaises(ValueError):
            self.inv.buscar("P001")


if __name__ == "__main__":
    unittest.main()
