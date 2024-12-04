import unittest

from main.core.update_database.update_database_service import UpdateDatabaseService
from tests.test_update_database.data.album_data_set import FIRST_LINE, ASTERIX_LIST
from tests.test_update_database.internal.database_in_memory import DatabaseInMemory
from tests.test_update_database.internal.sheet_in_memory import SheetInMemory


class TestUpdateDatabaseService(unittest.TestCase):

    TABLE_NAME = "BD"

    @classmethod
    def setUpClass(cls):
        cls.sheet_repository = SheetInMemory()
        cls.database_repository = DatabaseInMemory("")
        cls.service = UpdateDatabaseService(cls.sheet_repository, cls.database_repository)

    def setUp(self):
        self.sheet_repository.append(FIRST_LINE)
        self.sheet_repository.append(ASTERIX_LIST)

    def test_correctly_updated(self):
        self.service.main()
        database = self.database_repository.get_all(self.TABLE_NAME)
        self.assertEqual(1, len(database))
        self.assertEqual(len(FIRST_LINE), len(database[0]))
        self.assertEqual(FIRST_LINE, list(database[0].keys()))
        self.assertEqual(ASTERIX_LIST, list(database[0].values()))


if __name__ == '__main__':
    unittest.main()
