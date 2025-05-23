import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.infrastructure.persistence.database.models import BD
from main.core.common.database.internal.database_connexion import DatabaseConnexion
from tests.album_data_set import ALBUM_EXEMPLE


class TestDatabaseRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Before all
        cls.database_repository = DatabaseConnexion()
        BD.objects.all().delete()

    def tearDown(self) -> None:
        # After each
        BD.objects.all().delete()

    def test_insert_correctly(self) -> None:
        value = ALBUM_EXEMPLE
        self.database_repository.insert([value])
        entry = BD.objects.values('isbn',
                                  'album',
                                  'number',
                                  'series',
                                  'writer',
                                  'illustrator',
                                  'colorist',
                                  'publisher',
                                  'publication_date',
                                  'edition',
                                  'number_of_pages',
                                  'rating',
                                  'purchase_price',
                                  'year_of_purchase',
                                  'place_of_purchase',
                                  'deluxe_edition',
                                  'localisation',
                                  'synopsis',
                                  'image',
                                  ).get(isbn=value['isbn'])
        self.assertEqual(BD.objects.count(), 1)
        self.assertEqual(value, entry)

    def test_get_all_correctly(self) -> None:
        value = ALBUM_EXEMPLE.copy()
        obj = BD.objects.create(**value)
        entry = self.database_repository.get_all()
        value['id'] = obj.id
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry[0], value)

    def test_reset_table_correctly(self) -> None:
        value = ALBUM_EXEMPLE.copy()
        BD.objects.create(**value)
        self.database_repository.reset_table()
        self.assertEqual(BD.objects.count(), 0)


if __name__ == '__main__':
    unittest.main()
