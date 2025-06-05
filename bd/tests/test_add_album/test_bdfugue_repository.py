import unittest

from common.internal.logger_in_memory import LoggerInMemory
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.core.infrastructure.api.bd_fugue_adapter import BdFugueAdapter
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA, SAMBRE_ISBN, \
    SAMBRE_DATA, THORGAL_ISBN, THORGAL_DATA, SAULE_ISBN, SAULE_DATA


@unittest.skip("CI cannot access Cloudscraper")
class TestBdFugueRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdFugueAdapter(cls.logging_repository)

    def test_get_correct_url_from_isbn(self) -> None:
        self.bd_repository.isbn = ASTERIX_ISBN
        link = self.bd_repository.get_url()
        self.assertEqual(ASTERIX_URLS['BDFUGUE'], link)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(AlbumNotFoundException):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_isbn(self) -> None:
        infos = self.bd_repository.get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDFUGUE'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAMBRE_ISBN)
        self.assertEqual(SAMBRE_DATA['BDFUGUE'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self.bd_repository.get_infos(THORGAL_ISBN)
        self.assertEqual(THORGAL_DATA['BDFUGUE'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self.bd_repository.get_infos(SAULE_ISBN)
        self.assertEqual(SAULE_DATA['BDFUGUE'], infos)


if __name__ == '__main__':
    unittest.main()
