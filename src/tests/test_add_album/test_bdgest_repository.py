import os
import unittest

from curl_cffi import requests as cffi_requests

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.core.infrastructure.api.bd_gest_adapter import BdGestAdapter
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_URLS, ASTERIX_DATA, SAMBRE_DATA, \
    SAMBRE_ISBN, \
    THORGAL_DATA, THORGAL_ISBN, SAULE_ISBN, SAULE_DATA
from tests.test_common.internal.logger_in_memory import LoggerInMemory


@unittest.skipIf(
    os.getenv("CI") or os.getenv("GITHUB_ACTIONS"),
    "bedetheque.com bloque les IPs des runners GitHub Actions (HTTP 403)",
)
class TestBdGestRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdGestAdapter(cls.logging_repository)

    def _get_infos_or_skip(self, isbn: int):
        try:
            return self.bd_repository.get_infos(isbn)
        except cffi_requests.exceptions.RequestException:
            self.skipTest(f"bedetheque.com refuse la connexion pour ISBN {isbn}")

    def test_get_correct_url_from_isbn(self) -> None:
        self.bd_repository.isbn = ASTERIX_ISBN
        link = self.bd_repository.get_url()
        self.assertEqual(ASTERIX_URLS['BDGEST'], link)

    def test_get_correct_url_from_empty_isbn(self) -> None:
        self.bd_repository.isbn = 0
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_url()

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self._get_infos_or_skip(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_sambre_isbn(self) -> None:
        infos = self._get_infos_or_skip(SAMBRE_ISBN)
        self.assertEqual(SAMBRE_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_thorgal_isbn(self) -> None:
        infos = self._get_infos_or_skip(THORGAL_ISBN)
        self.assertEqual(THORGAL_DATA['BDGEST'], infos)

    def test_get_correct_infos_from_saule_isbn(self) -> None:
        infos = self._get_infos_or_skip(SAULE_ISBN)
        self.assertEqual(SAULE_DATA['BDGEST'], infos)


if __name__ == '__main__':
    unittest.main()
