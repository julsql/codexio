import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.internal.bdfugue_connexion import BdFugueRepository
from tests.test_add_album.data.album_data_set import ASTERIX_ISBN, ASTERIX_WEB, ASTERIX_BDFUGUE_LINK


class TestBdFugueRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bd_repository = BdFugueRepository()

    def test_get_correct_url_from_isbn(self):
        link = self.bd_repository.get_url(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_BDFUGUE_LINK, link)

    def test_get_no_infos_from_empty_isbn(self):
        with self.assertRaises(AddAlbumError):
            self.bd_repository.get_infos(0)


if __name__ == '__main__':
    unittest.main()
