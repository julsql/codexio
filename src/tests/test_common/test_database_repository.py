import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.models import AppUser
from main.core.infrastructure.persistence.database.table_bd_adapter import TableBdAdapter
from main.core.infrastructure.persistence.database.models.collection import Collection

from main.core.infrastructure.persistence.database.models.bd import BD
from tests.album_data_set import ALBUM_EXEMPLE, ALBUM_EXEMPLE_DICT


class TestDatabaseRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Before all
        cls.database_repository = TableBdAdapter()
        user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=user)
        cls.collection_id = cls.collection.id

        BD.objects.filter(collection=cls.collection).delete()

    def tearDown(self) -> None:
        # After each
        BD.objects.filter(collection=self.collection).delete()

    def test_insert_correctly(self) -> None:
        value = ALBUM_EXEMPLE
        self.database_repository.insert([value], self.collection)
        entry = (BD.objects.filter(collection=self.collection)
                 .values('isbn',
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
                         ).get(isbn=value.isbn))
        self.assertEqual(BD.objects.filter(collection=self.collection).count(), 1)
        self.assertEqual(ALBUM_EXEMPLE_DICT, entry)

    def test_get_all_correctly(self) -> None:
        value = ALBUM_EXEMPLE_DICT.copy()
        obj = BD.objects.create(**value, collection=self.collection)
        entry = self.database_repository.get_all(self.collection_id)
        value['id'] = obj.id
        value['collection_id'] = 1
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry[0], value)

    def test_reset_table_correctly(self) -> None:
        value = ALBUM_EXEMPLE_DICT
        BD.objects.create(**value, collection=self.collection)
        self.database_repository.reset_table(self.collection_id)
        self.assertEqual(BD.objects.filter(collection=self.collection).count(), 0)


if __name__ == '__main__':
    unittest.main()
