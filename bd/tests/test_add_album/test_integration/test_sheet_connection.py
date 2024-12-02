import unittest
from main.add_album.sheet_connection import Conn


class TestIntegration(unittest.TestCase):
    FIRST_LINE = [
    "ISBN", "Album", "Numéro", "Série", "Scénariste", "Dessinateur", "Couleur", "Éditeur", "Date de parution",
    "Édition", "Nombre de pages", "Cote", "Prix d'achat", "Année d'achat", "Lieu d'achat", "Tirage de tête",
    "Dédicace", "Ex Libris", "Synopsis", "Image"]

    def setUp(self):
        self.conn_test = Conn()
        self.conn_test.open("bd", "Test")

        self.conn_real = Conn()
        self.conn_real.open("bd")

    def tearDown(self):
        self.conn_test.delete_row(0)

    def test_add_cell_to_test_sheet(self):
        cell_value = "valeur test"
        self.conn_test.set(cell_value, 0, 0)
        cell_content = self.conn_test.get(0, 0)
        self.assertEqual(cell_value, cell_content)

    def test_add_row_to_test_sheet(self):
        self.conn_test.append(self.FIRST_LINE)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(self.FIRST_LINE, line_content)

    def test_add_and_delete_row_to_test_sheet(self):
        self.conn_test.append(self.FIRST_LINE)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(self.FIRST_LINE, line_content)

        self.conn_test.delete_row(0)
        full_content = self.conn_test.get_all()
        self.assertEqual([[]], full_content)

    def test_data_from_real_sheet(self):
        line_content = self.conn_real.get_line(0)
        self.assertEqual(self.FIRST_LINE, line_content)



if __name__ == '__main__':
    unittest.main()
