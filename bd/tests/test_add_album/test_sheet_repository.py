import unittest
from main.core.common.sheet_connexion import SheetConnexion
from tests.test_add_album.data.album_data_set import FIRST_LINE


class TestSheetRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn_test = SheetConnexion()
        cls.conn_test.open("bd", "Test")
        cls.conn_real = SheetConnexion()
        cls.conn_real.open("bd")

    def tearDown(self):
        self.conn_test.delete_row(0)

    def test_add_cell_to_test_sheet(self):
        cell_value = "valeur test"
        self.conn_test.set(cell_value, 0, 0)
        cell_content = self.conn_test.get(0, 0)
        self.assertEqual(cell_value, cell_content)

    def test_add_row_to_test_sheet(self):
        self.conn_test.append(FIRST_LINE)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(FIRST_LINE, line_content)

    def test_add_and_delete_row_to_test_sheet(self):
        self.conn_test.append(FIRST_LINE)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(FIRST_LINE, line_content)

        self.conn_test.delete_row(0)
        full_content = self.conn_test.get_all()
        self.assertEqual([[]], full_content)

    def test_data_from_real_sheet(self):
        line_content = self.conn_real.get_line(0)
        self.assertEqual(FIRST_LINE, line_content)



if __name__ == '__main__':
    unittest.main()
