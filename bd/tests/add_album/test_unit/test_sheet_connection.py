import unittest
from main.add_album.sheet_connection import Conn


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.logs = "logs-test-unit.txt"
        self.conn_test = Conn(self.logs)
        self.conn_test.open("bd", "Test")

        self.conn_real = Conn()
        self.conn_real.open("bd")

        self.first_line = [
            "ISBN", "Album", "Numéro", "Série", "Dessinateur", "Scénariste", "Couleur", "Éditeur", "Date de parution",
            "Édition", "Nombre de pages", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Dédicace",
            "Ex Libris", "Synopsis", "Image"]

    def test_get_data_from_test_sheet(self):
        cell_value = "valeur test"
        self.conn_test.set(cell_value, 0, 0)
        cell_content = self.conn_test.get(0, 0)
        self.assertEqual(cell_content, cell_value)
        self.conn_test.set("", 0, 0)

        self.conn_test.append(self.first_line)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(line_content, self.first_line)

        self.conn_test.set_line([""] * 19, 0)

        full_content = self.conn_test.get_all()
        self.assertEqual(full_content, [])

    def test_data_from_real_sheet(self):
        line_content = self.conn_real.get_line(0)
        self.assertEqual(line_content, self.first_line)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
