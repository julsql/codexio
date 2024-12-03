import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from tests.test_add_album.data.album_data_set import ASTERIX_ISBN, ASTERIX_WEB, ASTERIX_BDPHILE_LINK


class TestBdPhileRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bd_repository = BdPhileRepository()

    def test_get_correct_url_from_isbn(self):
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_BDPHILE_LINK, link)

    def test_get_correct_url_from_empty_isbn(self):
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_url(0)

    def test_get_no_infos_from_empty_isbn(self):
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_isbn(self):
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_WEB, infos)

if __name__ == '__main__':
    unittest.main()
