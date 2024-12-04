import unittest
from main.core.common.sheet.internal.sheet_connexion import SheetConnexion
from tests.album_data_set import FIRST_LINE, ASTERIX_LIST, ASTERIX_ISBN, ASTERIX_LIST_STR


class TestSheetRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn_test = SheetConnexion()
        cls.conn_test.open("bd", "Test")
        cls.conn_real = SheetConnexion()
        cls.conn_real.open("bd")

    def tearDown(self):
        self.conn_test.clear()

    def test_get_size(self):
        self.conn_test.append(FIRST_LINE)
        self.conn_test.append(ASTERIX_LIST)
        self.assertEqual((2, len(FIRST_LINE)), self.conn_test.get_size())

    def test_add_cell_to_test_sheet(self):
        cell_value = "valeur test"
        self.conn_test.set(cell_value, 0, 0)
        cell_content = self.conn_test.get(0, 0)
        self.assertEqual(cell_value, cell_content)

    def test_add_incorrect_cell_to_test_sheet(self):
        cell_value = {1: [True]}
        with self.assertRaises(TypeError):
            self.conn_test.set(cell_value, 0, 0)

    def test_add_row_to_test_sheet(self):
        self.conn_test.append(FIRST_LINE)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(FIRST_LINE, line_content)

    def test_get_column_to_test_sheet(self):
        self.conn_test.append(FIRST_LINE)
        self.conn_test.append(ASTERIX_LIST)
        column_index = 0
        column_content = self.conn_test.get_column(column_index)
        self.assertEqual(2, len(column_content))
        self.assertEqual([str(FIRST_LINE[column_index]), str(ASTERIX_LIST[column_index])], column_content)

    def test_add_and_delete_row_to_test_sheet(self):
        self.conn_test.append(FIRST_LINE)
        line_content = self.conn_test.get_line(0)
        self.assertEqual(FIRST_LINE, line_content)

        self.conn_test.delete_row(0)
        full_content = self.conn_test.get_all()
        self.assertEqual([[]], full_content)

    def test_set_column_to_test_sheet(self):
        column = ["value1", "value2"]
        column_index = 0
        self.conn_test.set_column(column, column_index, 0)
        column_content = self.conn_test.get_column(column_index)
        self.assertEqual(column, column_content)

    def test_set_line_to_test_sheet(self):
        line_index = 0
        self.conn_test.set_line(ASTERIX_LIST, line_index)
        line_content = self.conn_test.get_line(line_index)
        self.assertEqual(ASTERIX_LIST_STR, line_content)

    def test_album_existing_from_test_sheet(self):
        self.conn_test.append(ASTERIX_LIST)
        self.assertTrue(self.conn_test.double(ASTERIX_ISBN))

    def test_album_inexistant_from_test_sheet(self):
        self.assertFalse(self.conn_test.double(ASTERIX_ISBN))

    def test_data_from_real_sheet(self):
        line_content = self.conn_real.get_line(0)
        self.assertEqual(FIRST_LINE, line_content)



if __name__ == '__main__':
    unittest.main()
