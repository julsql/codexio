import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.get_infos_service import GetInfosService
from tests.album_data_set import ASTERIX_ISBN, ASTERIX
from tests.test_add_album.internal.bd_in_memory import BdInMemory


class TestCorrectInfos(unittest.TestCase):

    INEXISTANT_ISBN = 9791038203907

    @classmethod
    def setUpClass(cls):
        cls.repository = BdInMemory()


    def test_get_correct_info_successfully(self):
        self.service = GetInfosService([])
        self.service.isbn = 0
        info = self.service.corriger_info({})
        self.assertEqual({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''},
            info)

    def test_raise_error_correct_empty_value(self):
        self.service = GetInfosService([])
        self.service.isbn = 0
        with self.assertRaises(AttributeError):
            self.service.corriger_info("")

    def test_get_info_from_isbn_successfully(self):
        self.service = GetInfosService([self.repository])
        info = self.service.main(ASTERIX_ISBN)
        self.assertEqual(ASTERIX, info)

    def test_raise_error_get_info_from_inexistant_isbn(self):
        self.service = GetInfosService([])
        with self.assertRaises(AddAlbumError):
            self.service.main(self.INEXISTANT_ISBN)



if __name__ == '__main__':
    unittest.main()
