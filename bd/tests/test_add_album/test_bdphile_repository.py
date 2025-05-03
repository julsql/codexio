import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdphile_connexion import BdPhileRepository
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA, SAMBRE_ISBN, \
    SAMBRE_DATA, \
    THORGAL_ISBN, THORGAL_DATA, SAULE_ISBN, SAULE_DATA


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

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAMBRE_ISBN)
        self.assertEqual(SAMBRE_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self.bd_repository.get_infos(THORGAL_ISBN)
        self.assertEqual(THORGAL_DATA['BDPHILE'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAULE_ISBN)
        self.assertEqual(SAULE_DATA['BDPHILE'], infos)


if __name__ == '__main__':
    unittest.main()
