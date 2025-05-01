import unittest

from main.core.common.sheet.internal.sheet_in_memory import SheetInMemory
from main.core.update_database.update_database_service import UpdateDatabaseService
from tests.album_data_set import FIRST_LINE, ASTERIX_LIST, FIRST_LINE_DATABASE, ASTERIX_LIST_RESULT
from tests.test_common.internal.database_in_memory import DatabaseInMemory


class TestUpdateDatabaseService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.sheet_repository = SheetInMemory()
        cls.database_repository = DatabaseInMemory()
        cls.service = UpdateDatabaseService(cls.sheet_repository, cls.database_repository)

    def setUp(self) -> None:
        self.sheet_repository.append(FIRST_LINE)
        self.sheet_repository.append(ASTERIX_LIST)

    def test_correctly_updated(self) -> None:
        self.service.main()
        database = self.database_repository.get_all()
        self.assertEqual(1, len(database))
        self.assertEqual(len(FIRST_LINE_DATABASE), len(database[0]))
        self.assertEqual(FIRST_LINE_DATABASE, list(database[0].keys()))
        self.assertEqual(ASTERIX_LIST_RESULT, list(database[0].values()))


if __name__ == '__main__':
    unittest.main()
