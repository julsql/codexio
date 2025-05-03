import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdgest_connexion import BdGestRepository
from test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA, SAMBRE_DATA, SAMBRE_ISBN, \
    THORGAL_DATA, THORGAL_ISBN, SAULE_ISBN, SAULE_DATA


class TestBdGestRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bd_repository = BdGestRepository()

    def test_get_correct_url_from_isbn(self) -> None:
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_URLS['BDGEST'], link)

    def test_get_correct_url_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_url(0)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAMBRE_ISBN)
        self.assertEqual(SAMBRE_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self.bd_repository.get_infos(THORGAL_ISBN)
        self.assertEqual(THORGAL_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAULE_ISBN)
        self.assertEqual(SAULE_DATA['BDGEST'], infos)


if __name__ == '__main__':
    unittest.main()
