import unittest

from main.add_album import error
from main.add_album import sheet_add_album
from tests.test_add_album.data.album_data_set import ASTERIX, ASTERIX_ISBN, ASTERIX_LIST
from tests.test_add_album.internal import add_album_in_memory
from tests.test_add_album.internal.connection_in_memory import ConnInMemory


class TestIntegration(unittest.TestCase):
    NB_COLUMN = 20
    DOC_NAME = "bd"
    SHEET = "Test"

    def setUp(self):
        # Before each
        self.connection = ConnInMemory()
        self.connection.open(self.DOC_NAME, self.SHEET)

    def tearDown(self):
        # After each
        self.connection.delete_row(0)

    def test_convert_list_from_dict_empty_value_successfully(self):
        liste = sheet_add_album.liste_from_dict({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''})
        self.assertEqual([""] * self.NB_COLUMN, liste)

    def test_convert_list_from_dict_successfully(self):
        liste = sheet_add_album.liste_from_dict({
            'Album': 'a', 'Couleurs': 'a', 'Date de publication': 'a',
            'Dessin': 'a', 'Édition': 'a', 'ISBN': 'a', 'Image': 'a',
            'Numéro': 'a', 'Pages': 'a', 'Prix': 'a', 'Scénario': 'a',
            'Synopsis': 'a', 'Série': 'a', 'Éditeur': 'a'})
        self.assertEqual(["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "", "a", "", "", "", "", "", "a", "a"],
                         liste)

    def test_raise_error_convert_list_from_empty_dict(self):
        with self.assertRaises(IndexError):
            sheet_add_album.liste_from_dict({})

    def test_add_album_successfully(self):
        self.assertEqual(ASTERIX, add_album_in_memory.add_album(ASTERIX_ISBN, self.DOC_NAME, self.SHEET))
        sheet_line = self.connection.get_line(0)
        self.assertEqual(ASTERIX_LIST, sheet_line)

    def test_raise_error_on_incorrect_docname(self):
        with self.assertRaises(error.Error):
            add_album_in_memory.add_album(ASTERIX_ISBN, "youhou", None)

    def test_raise_error_on_incorrect_sheetname(self):
        with self.assertRaises(error.Error):
            add_album_in_memory.add_album(ASTERIX_ISBN, self.DOC_NAME, "sheet")

    def test_raise_error_on_duplicate_isbn(self):
        add_album_in_memory.add_album(ASTERIX_ISBN, self.DOC_NAME, self.SHEET)
        with self.assertRaises(error.Error):
            add_album_in_memory.add_album(ASTERIX_ISBN, self.DOC_NAME, self.SHEET)


if __name__ == '__main__':
    unittest.main()
