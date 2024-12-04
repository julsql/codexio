import unittest

from main.core.existing_album.existing_album_service import ExistingAlbumService
from tests.test_existing_album.data.album_data_set import ASTERIX_LIST, ASTERIX_ISBN
from tests.test_existing_album.internal.sheet_in_memory import SheetInMemory


class TestExistingAlbumService(unittest.TestCase):

    INEXISTANT_ISBN = 9791038203907

    @classmethod
    def setUpClass(cls):
        sheet_repository = SheetInMemory()
        sheet_repository.append(ASTERIX_LIST)
        cls.service = ExistingAlbumService(sheet_repository)

    def test_already_exists(self):
        self.assertTrue(self.service.main(ASTERIX_ISBN))

    def test_dont_exists(self):
        self.assertFalse(self.service.main(self.INEXISTANT_ISBN))


if __name__ == '__main__':
    unittest.main()
