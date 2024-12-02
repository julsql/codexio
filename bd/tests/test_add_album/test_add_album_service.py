import unittest

from main.core.add_album.add_album_service import AddAlbumService
from tests.test_add_album.internal.bd_in_memory import BdInMemory
from tests.test_add_album.internal.gsheet_in_memory import GsheetInMemory


class TestAddAlbumService(unittest.TestCase):

    def setUp(self):
        isbn = 1234
        gsheet_repository = GsheetInMemory()
        bd_repository = BdInMemory()
        service = AddAlbumService(isbn, [bd_repository], gsheet_repository)


if __name__ == '__main__':
    unittest.main()
