import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound, ApiConnexionException
from main.core.infrastructure.api.book_adapter import BookAdapter
from tests.test_add_album.book_large_data_set import BOVARY_ISBN, BOVARY_DATA
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestBookRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BookAdapter(cls.logging_repository)

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

    def test_get_correct_infos_from_bovary_isbn(self) -> None:
        infos = self._get_infos_or_skip(BOVARY_ISBN)
        expected = BOVARY_DATA['BOOK']

        self.assertRegex(
            infos.image,
            r"^http://books\.google\.com/books/content\?id=[^&]+&printsec=frontcover&img=1&zoom=1&source=gbs_api$",
        )

        actual_without_image = infos.copy()
        actual_without_image.image = ""
        expected_without_image = expected.copy()
        expected_without_image.image = ""
        self.assertEqual(expected_without_image, actual_without_image)



if __name__ == '__main__':
    unittest.main()
