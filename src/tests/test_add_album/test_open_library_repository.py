import os
import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.core.infrastructure.api.open_library_adapter import OpenLibraryAdapter
from tests.test_add_album.book_large_data_set import BOVARY_ISBN
from tests.test_common.internal.logger_in_memory import LoggerInMemory


@unittest.skipIf(
    os.getenv("CI") or os.getenv("GITHUB_ACTIONS"),
    "OpenLibrary renvoie une edition par ISBN dont les contributeurs varient (auteur parfois absent)",
)
class TestOpenLibraryRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.book_repository = OpenLibraryAdapter(cls.logging_repository)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.book_repository.get_infos(0)

    def test_get_correct_infos_from_bovary_isbn(self) -> None:
        infos = self.book_repository.get_infos(BOVARY_ISBN)

        self.assertEqual(BOVARY_ISBN, infos.isbn)
        self.assertEqual("Madame Bovary : moeurs de province", infos.title)
        self.assertIn("Gustave Flaubert", infos.writer)
        self.assertEqual("Gallimard", infos.publisher)
        self.assertEqual("Collection Folio classique", infos.collection_book)
        self.assertEqual("fr", infos.origin_language)
        self.assertEqual(513, infos.number_of_pages)
        self.assertRegex(
            infos.image,
            r"^https://covers\.openlibrary\.org/b/id/\d+-L\.jpg$",
        )
        self.assertIn("Charles Bovary", infos.synopsis)


if __name__ == "__main__":
    unittest.main()
