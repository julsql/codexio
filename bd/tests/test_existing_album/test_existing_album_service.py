import unittest

from common.internal.sheet_in_memory import SheetInMemory
from main.application.usecases.existing_album.existing_album_service import ExistingAlbumService
from test_add_album.album_large_data_set import ASTERIX_ISBN
from tests.album_data_set import ASTERIX_LIST


class TestExistingAlbumService(unittest.TestCase):
    INEXISTANT_ISBN = 9791038203907

    @classmethod
    def setUpClass(cls) -> None:
        sheet_repository = SheetInMemory()
        sheet_repository.append(ASTERIX_LIST)
        cls.service = ExistingAlbumService(sheet_repository)

    def test_already_exists(self) -> None:
        self.assertTrue(self.service.execute(ASTERIX_ISBN))

    def test_does_not_exists(self) -> None:
        self.assertFalse(self.service.execute(self.INEXISTANT_ISBN))


if __name__ == '__main__':
    unittest.main()
