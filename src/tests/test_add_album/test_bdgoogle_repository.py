import os
import unittest
from unittest.mock import MagicMock, patch

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.infrastructure.api.bd_google_adapter import BdGoogleAdapter
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN, ASTERIX_DATA, SAMBRE_DATA, SAMBRE_ISBN, \
    THORGAL_DATA, THORGAL_ISBN, SAULE_ISBN, SAULE_DATA
from tests.test_add_album.google_books_responses import fake_google_books_get, http_error_response
from tests.test_common.internal.logger_in_memory import LoggerInMemory

REQUESTS_GET = "main.core.infrastructure.api.bd_google_adapter.requests.get"


@patch(REQUESTS_GET, side_effect=fake_google_books_get)
class TestBdGoogleRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.bd_repository = BdGoogleAdapter(LoggerInMemory())

    def test_queries_google_books_by_isbn(self, requests_get: MagicMock) -> None:
        self.bd_repository.get_infos(ASTERIX_ISBN)

        requests_get.assert_called_once()
        url, = requests_get.call_args.args
        params = requests_get.call_args.kwargs["params"]
        self.assertEqual("https://www.googleapis.com/books/v1/volumes", url)
        self.assertEqual(f"isbn:{ASTERIX_ISBN}", params["q"])
        self.assertEqual("FR", params["country"])
        self.assertIn("key", params)

    def test_get_no_infos_from_empty_isbn(self, _: MagicMock) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_infos(0)

    def test_raises_connexion_exception_on_http_error(self, requests_get: MagicMock) -> None:
        requests_get.side_effect = None
        requests_get.return_value = http_error_response(429, "Quota exceeded")
        with self.assertRaises(ApiConnexionException):
            self.bd_repository.get_infos(ASTERIX_ISBN)

    def test_get_correct_infos_from_asterix_isbn(self, _: MagicMock) -> None:
        self.assertEqual(ASTERIX_DATA['BDGOOGLE'], self.bd_repository.get_infos(ASTERIX_ISBN))

    def test_get_correct_infos_from_sambre_isbn(self, _: MagicMock) -> None:
        self.assertEqual(SAMBRE_DATA['BDGOOGLE'], self.bd_repository.get_infos(SAMBRE_ISBN))

    def test_get_correct_infos_from_thorgal_isbn(self, _: MagicMock) -> None:
        self.assertEqual(THORGAL_DATA['BDGOOGLE'], self.bd_repository.get_infos(THORGAL_ISBN))

    def test_get_correct_infos_from_saule_isbn(self, _: MagicMock) -> None:
        self.assertEqual(SAULE_DATA['BDGOOGLE'], self.bd_repository.get_infos(SAULE_ISBN))


@unittest.skipUnless(
    os.getenv("GOOGLE_BOOKS_LIVE_TESTS") == "1",
    "Test d'intégration réel Google Books : activer avec GOOGLE_BOOKS_LIVE_TESTS=1",
)
class TestBdGoogleRepositoryLive(unittest.TestCase):
    def test_finds_asterix_on_google_books(self) -> None:
        album = BdGoogleAdapter(LoggerInMemory()).get_infos(ASTERIX_ISBN)
        self.assertEqual(ASTERIX_ISBN, album.isbn)
        self.assertNotEqual("", album.title)


if __name__ == '__main__':
    unittest.main()
