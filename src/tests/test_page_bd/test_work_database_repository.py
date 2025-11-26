import datetime
import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.infrastructure.persistence.database.models.bd import BD as DATABASE_MODEL_BD
from main.core.infrastructure.persistence.database.page_bd_database_adapter import WorkDatabaseBdAdapter
from main.core.infrastructure.persistence.database.models.collection import Collection
from main.models import AppUser


class TestWorkDatabaseConnexion(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.repository = WorkDatabaseBdAdapter()
        cls.EXPECTED_FIELDS = {
            'isbn': 'isbn',
            'album': 'title',
            'number': 'number',
            'series': 'series',
            'writer': 'writer',
            'illustrator': 'illustrator',
            'colorist': 'colorist',
            'publisher': 'publisher',
            'publication_date': 'publication_date',
            'edition': 'edition',
            'number_of_pages': 'number_of_pages',
            'purchase_price': 'purchase_price',
            'year_of_purchase': 'year_of_purchase',
            'place_of_purchase': 'place_of_purchase',
            'synopsis': 'synopsis',
            'image': 'image',
        }
        user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=user)
        cls.collection_id = cls.collection.id

    def setUp(self) -> None:
        DATABASE_MODEL_BD.objects.filter(collection=self.collection).delete()

    def test_page_with_non_existing_isbn(self) -> None:
        # Act
        result = self.repository.page(1234, self.collection_id)

        # Assert
        self.assertIsNone(result)

    def test_page_with_existing_bd(self) -> None:
        # Arrange
        test_data = {
            'isbn': 5678,
            'album': 'Test Album 2',
            'number': '2',
            'series': 'Test Series 2',
            'writer': 'Test Writer 2',
            'illustrator': 'Test Illustrator 2',
            'colorist': 'Test Colorist 2',
            'publisher': 'Test Publisher 2',
            'publication_date': datetime.date(2025, 1, 1),
            'edition': '1',
            'number_of_pages': 48,
            'purchase_price': 15.99,  # Prix décimal
            'year_of_purchase': 2023,
            'place_of_purchase': 'Test Store 2',
            'synopsis': 'Test Synopsis 2',
            'image': 'test2.jpg',
            'deluxe_edition': False,
        }
        DATABASE_MODEL_BD.objects.create(**test_data,
                                         collection=self.collection)

        # Act
        result = self.repository.page(5678, self.collection_id)

        # Assert
        self.assertIsNotNone(result)
        # Vérifie que le prix est resté décimal
        self.assertEqual(15.99, float(result.purchase_price))
        # Vérifie tous les autres champs
        filtered_fields = {
            k: v for k, v in self.EXPECTED_FIELDS.items() if k != 'purchase_price'
        }
        for key, value in filtered_fields.items():
            self.assertEqual(test_data[key], getattr(result, value))

    def test_page_with_null_fields(self) -> None:
        # Arrange
        test_data = {
            'isbn': 9012,
            'album': 'Test Album',
            'deluxe_edition': False,
        }

        DATABASE_MODEL_BD.objects.create(**test_data,
                                         collection=self.collection)

        # Act
        result = self.repository.page(9012, self.collection_id)

        # Assert
        self.assertIsNotNone(result)
        for key, value in self.EXPECTED_FIELDS.items():
            if key in ['isbn', 'album', 'deluxe_edition']:
                self.assertEqual(test_data[key], getattr(result, value))
            else:
                self.assertIn(getattr(result, value), [None, ''])

    def test_page_with_multiple_bds(self) -> None:
        # Arrange
        test_data_list = [
            {
                'isbn': 1111,
                'album': 'Album 1',
                'purchase_price': 10.0,
                'deluxe_edition': False,
            },
            {
                'isbn': 2222,
                'album': 'Album 2',
                'purchase_price': 12.5,
                'deluxe_edition': False,
            },
        ]
        for data in test_data_list:
            DATABASE_MODEL_BD.objects.create(**data,
                                             collection=self.collection)

        # Act & Assert
        for test_data in test_data_list:
            result = self.repository.page(int(test_data['isbn']), self.collection_id)
            self.assertIsNotNone(result)
            self.assertEqual(test_data['album'], result.title)
            self.assertEqual(test_data['isbn'], result.isbn)
            if test_data['purchase_price'].is_integer():
                self.assertEqual(int(test_data['purchase_price']), result.purchase_price)
            else:
                self.assertEqual(test_data['purchase_price'], result.purchase_price)


if __name__ == '__main__':
    unittest.main()
