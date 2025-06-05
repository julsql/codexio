import unittest

from main.core.application.usecases.update_database.update_database_service import UpdateDatabaseService
from tests.album_data_set import FIRST_LINE_SHEET, ASTERIX_LIST, ASTERIX_ALBUM
from tests.test_common.internal.database_in_memory import DatabaseInMemory
from tests.test_common.internal.sheet_in_memory import SheetInMemory


class TestUpdateDatabaseService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.sheet_repository = SheetInMemory()
        cls.database_repository = DatabaseInMemory()
        cls.service = UpdateDatabaseService(cls.sheet_repository, cls.database_repository)

    def setUp(self) -> None:
        self.sheet_repository.append(FIRST_LINE_SHEET)
        self.sheet_repository.append(ASTERIX_LIST)

    def test_correctly_updated(self) -> None:
        self.service.main()
        database = self.database_repository.get_all()
        self.assertEqual(1, len(database))
        self.assertEqual(ASTERIX_ALBUM, database[0])


if __name__ == '__main__':
    unittest.main()
