import unittest
from datetime import date

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.core.infrastructure.api.bnf_adapter import BnfAdapter
from tests.test_add_album.book_large_data_set import BOVARY_ISBN
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestBnfRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.book_repository = BnfAdapter(cls.logging_repository)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.book_repository.get_infos(0)

    def test_get_correct_infos_from_bovary_isbn(self) -> None:
        infos = self.book_repository.get_infos(BOVARY_ISBN)

        self.assertEqual(BOVARY_ISBN, infos.isbn)
        self.assertEqual("Madame Bovary : moeurs de province", infos.title)
        self.assertEqual("Gustave Flaubert", infos.writer)
        self.assertEqual("Gallimard", infos.publisher)
        self.assertEqual("Collection Folio", infos.collection_book)
        self.assertEqual(date(2001, 1, 1), infos.publication_date)
        self.assertEqual(513, infos.number_of_pages)
        self.assertEqual("fr", infos.origin_language)


if __name__ == "__main__":
    unittest.main()
