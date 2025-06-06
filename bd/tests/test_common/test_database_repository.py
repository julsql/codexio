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
        cls.user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=cls.user)

        BD.objects.filter(collection__accounts=cls.user).delete()

    def tearDown(self) -> None:
        # After each
        BD.objects.filter(collection__accounts=self.user).delete()

    def test_insert_correctly(self) -> None:
        value = ALBUM_EXEMPLE
        self.database_repository.insert([value], self.user)
        entry = (BD.objects.filter(collection__accounts=self.user)
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
        self.assertEqual(BD.objects.filter(collection__accounts=self.user).count(), 1)
        self.assertEqual(ALBUM_EXEMPLE_DICT, entry)

    def test_get_all_correctly(self) -> None:
        value = ALBUM_EXEMPLE_DICT.copy()
        obj = BD.objects.create(**value, collection=self.collection)
        entry = self.database_repository.get_all(self.user)
        value['id'] = obj.id
        value['collection_id'] = 1
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry[0], value)

    def test_reset_table_correctly(self) -> None:
        value = ALBUM_EXEMPLE_DICT
        BD.objects.create(**value, collection=self.collection)
        user = AppUser.objects.get(username='admin')
        self.database_repository.reset_table(user)
        self.assertEqual(BD.objects.filter(collection__accounts=self.user).count(), 0)


if __name__ == '__main__':
    unittest.main()
