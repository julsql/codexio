import os
import unittest
from unittest.mock import MagicMock, patch

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.infrastructure.api.book_adapter import BookAdapter
from tests.test_add_album.book_large_data_set import BOVARY_ISBN, BOVARY_DATA
from tests.test_add_album.google_books_responses import fake_google_books_get, http_error_response
from tests.test_common.internal.logger_in_memory import LoggerInMemory

REQUESTS_GET = "main.core.infrastructure.api.book_adapter.requests.get"


@patch(REQUESTS_GET, side_effect=fake_google_books_get)
class TestBookRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.book_repository = BookAdapter(LoggerInMemory())

    def test_queries_google_books_by_isbn(self, requests_get: MagicMock) -> None:
        self.book_repository.get_infos(BOVARY_ISBN)

        requests_get.assert_called_once()
        params = requests_get.call_args.kwargs["params"]
        self.assertEqual(f"isbn:{BOVARY_ISBN}", params["q"])
        self.assertIn("key", params)

    def test_get_no_infos_from_empty_isbn(self, _: MagicMock) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.book_repository.get_infos(0)

    def test_raises_connexion_exception_on_http_error(self, requests_get: MagicMock) -> None:
        requests_get.side_effect = None
        requests_get.return_value = http_error_response(503, "Service temporarily unavailable")
        with self.assertRaises(ApiConnexionException):
            self.book_repository.get_infos(BOVARY_ISBN)

    def test_get_correct_infos_from_bovary_isbn(self, _: MagicMock) -> None:
        self.assertEqual(BOVARY_DATA['BOOK'], self.book_repository.get_infos(BOVARY_ISBN))


@unittest.skipUnless(
    os.getenv("GOOGLE_BOOKS_LIVE_TESTS") == "1",
    "Test d'intégration réel Google Books : activer avec GOOGLE_BOOKS_LIVE_TESTS=1",
)
class TestBookRepositoryLive(unittest.TestCase):
    def test_finds_bovary_on_google_books(self) -> None:
        book = BookAdapter(LoggerInMemory()).get_infos(BOVARY_ISBN)
        self.assertEqual(BOVARY_ISBN, book.isbn)
        self.assertNotEqual("", book.title)


if __name__ == '__main__':
    unittest.main()
