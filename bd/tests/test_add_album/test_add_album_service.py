import unittest
from datetime import date
from decimal import Decimal

from common.internal.logger_in_memory import LoggerInMemory
from common.internal.sheet_in_memory import SheetInMemory
from main.application.usecases.add_album.add_album_service import AddAlbumService
from main.domain.exceptions.album_exceptions import AlbumAlreadyExistsException, AlbumNotFoundException
from main.domain.model.album import Album
from test_add_album.album_large_data_set import ASTERIX_ISBN
from tests.album_data_set import ASTERIX
from tests.test_add_album.internal.bd_in_memory import BdInMemory


class TestAddAlbumService(unittest.TestCase):
    NB_COLUMN = 21

    @classmethod
    def setUpClass(cls) -> None:
        # Before all
        cls.sheet_repository = SheetInMemory()
        cls.logging_repository = LoggerInMemory()
        cls.bd_repository = BdInMemory("AddAlbumBdRepository", ASTERIX)
        cls.service = AddAlbumService([cls.bd_repository], cls.sheet_repository, cls.logging_repository)

    def tearDown(self) -> None:
        # After each
        self.sheet_repository.clear()

    def test_convert_list_from_dict_empty_value_successfully(self) -> None:
        liste = self.service.map_to_list(Album(isbn=0))
        expected = [0 if i == 0 else "" for i in range(self.NB_COLUMN)]
        self.assertEqual(expected, liste)

    def test_convert_list_from_dict_successfully(self) -> None:
        album = Album(isbn=0)
        album.title = "a"
        album.number = "a"
        album.series = "a"
        album.writer = "a"
        album.illustrator = "a"
        album.colorist = "a"
        album.publisher = "a"
        album.publication_date = date(1900, 1, 1)
        album.edition = "a"
        album.number_of_pages = 10
        album.purchase_price = Decimal("10")
        album.synopsis = "a"
        album.image = "a"
        liste = self.service.map_to_list(album)
        self.assertEqual(
            [0, "a", "a", "a", "a", "a", "a", "a", "1 janv. 1900", "a", 10, "", 10.0, "", "", "", "", "", "", "a", "a"],
            liste)

    def test_add_album_successfully(self) -> None:
        self.service.isbn = ASTERIX_ISBN
        self.assertEqual(ASTERIX, self.service.get_infos())

    def test_raise_error_on_duplicate_isbn(self) -> None:
        self.service.main(ASTERIX_ISBN)
        with self.assertRaises(AlbumAlreadyExistsException):
            self.service.main(ASTERIX_ISBN)

    def test_raise_error_get_info_from_incorrect_isbn(self) -> None:
        with self.assertRaises(AlbumNotFoundException):
            self.service.main(0)


if __name__ == '__main__':
    unittest.main()
