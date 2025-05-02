import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from tests.album_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA


class TestBdPhileRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bd_repository = BdPhileRepository()

    def test_get_correct_url_from_isbn(self) -> None:
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_URLS['BDPHILE'], link)

    def test_get_correct_url_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_url(0)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDPHILE'], infos)


if __name__ == '__main__':
    unittest.main()
