import unittest

from main.core.domain.exceptions.api_exceptions import ApiConnexionDataNotFound
from main.core.infrastructure.api.book_adapter import BookAdapter
from tests.test_add_album.book_large_data_set import BOVARY_ISBN, BOVARY_DATA
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestBdPhileRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BookAdapter(cls.logging_repository)

    def test_get_no_infos_from_empty_isbn(self) -> None:
        with self.assertRaises(ApiConnexionDataNotFound):
            self.bd_repository.get_infos(0)

    def test_get_correct_infos_from_asterix_isbn(self) -> None:
        infos = self.bd_repository.get_infos(BOVARY_ISBN)
        self.assertEqual(BOVARY_DATA['BOOK'], infos)



if __name__ == '__main__':
    unittest.main()
