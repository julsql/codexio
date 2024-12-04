import unittest

from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion


class TestDatabaseRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database_file = DATABASES['test']['NAME']
        cls.database = DatabaseConnexion(database_file)
        cls.database.open()

    def tearDown(self):
        self.database.close()

if __name__ == '__main__':
    unittest.main()
