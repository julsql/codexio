import unittest

from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion


class TestDatabaseRepository(unittest.TestCase):
    TABLE_NAME = "test_table"
    COLUMN_NAME = ["column1", "column2"]

    @classmethod
    def setUpClass(cls):
        database_file = DATABASES['test']['NAME']
        cls.database = DatabaseConnexion(database_file)

    def setUp(self):
        self.database.open()

    def tearDown(self):
        self.database.close()

    def test_create_table(self):
        self.database.create_table(self.TABLE_NAME, self.COLUMN_NAME)
        self.assertEqual([], self.database.get_all(self.TABLE_NAME))

    def test_create_and_fill_table(self):
        first_row = ["value1", "value2"]
        second_row = ["value3", "value4"]
        self.database.create_table(self.TABLE_NAME, self.COLUMN_NAME)
        self.database.insert(self.TABLE_NAME, self.COLUMN_NAME, [first_row, second_row])
        content = self.database.get_all(self.TABLE_NAME)
        self.assertEqual(2, len(content))
        self.assertEqual(first_row[0], content[0][self.COLUMN_NAME[0]])

if __name__ == '__main__':
    unittest.main()
