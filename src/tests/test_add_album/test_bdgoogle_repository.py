import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.infrastructure.api.bd_google_adapter import BdGoogleAdapter
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_DATA, SAMBRE_DATA, SAMBRE_ISBN, \
    THORGAL_DATA, THORGAL_ISBN, SAULE_ISBN, SAULE_DATA
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestBdGoogleRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdGoogleAdapter(cls.logging_repository)

    def _get_infos_or_skip(self, isbn: int):
        try:
            return self.bd_repository.get_infos(isbn)
        except ApiConnexionException as exc:
            message = str(exc)
            if '503' in message or 'Service temporarily unavailable' in message:
                self.skipTest(f"Google Books API indisponible (503) pour ISBN {isbn}")
            raise

    def test_get_no_infos_from_empty_isbn(self) -> None:
        try:
            with self.assertRaises(ApiConnexionDataNotFound):
                self.bd_repository.get_infos(0)
        except ApiConnexionException as exc:
            message = str(exc)
            if '503' in message or 'Service temporarily unavailable' in message:
                self.skipTest("Google Books API indisponible (503)")
            raise

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self._get_infos_or_skip(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDGOOGLE'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self._get_infos_or_skip(SAMBRE_ISBN)
        self.assertEqual(SAMBRE_DATA['BDGOOGLE'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self._get_infos_or_skip(THORGAL_ISBN)
        self.assertEqual(THORGAL_DATA['BDGOOGLE'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self._get_infos_or_skip(SAULE_ISBN)
        self.assertEqual(SAULE_DATA['BDGOOGLE'], infos)


if __name__ == '__main__':
    unittest.main()
