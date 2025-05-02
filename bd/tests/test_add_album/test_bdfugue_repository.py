import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdfugue_connexion import BdFugueRepository
from tests.album_data_set import ASTERIX_ISBN, ASTERIX_BDFUGUE_LINK, ASTERIX_WEB_FUGUE


class TestBdFugueRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bd_repository = BdFugueRepository()

    def test_get_correct_url_from_isbn(self) -> None:
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_BDFUGUE_LINK, link)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_WEB_FUGUE, infos)


if __name__ == '__main__':
    unittest.main()
