import datetime
import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.infrastructure.persistence.database.models import BD
from main.core.page_bd.internal.page_bd_database_connexion import PageBdDatabaseConnexion


class TestPageBdDatabaseConnexion(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.repository = PageBdDatabaseConnexion()
        cls.EXPECTED_FIELDS = {
            'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist',
            'publisher', 'publication_date', 'edition', 'number_of_pages',
            'purchase_price', 'year_of_purchase', 'place_of_purchase',
            'synopsis', 'image'
        }

    def setUp(self) -> None:
        BD.objects.all().delete()

    def test_page_with_non_existing_isbn(self) -> None:
        # Act
        result = self.repository.page(1234)

        # Assert
        self.assertIsNone(result)

    def test_page_with_existing_bd_integer_price(self) -> None:
        # Arrange
        test_data = {
            'isbn': 1234,
            'album': 'Test Album',
            'number': '1',
            'series': 'Test Series',
            'writer': 'Test Writer',
            'illustrator': 'Test Illustrator',
            'colorist': 'Test Colorist',
            'publisher': 'Test Publisher',
            'publication_date': datetime.date(2025, 1, 1),
            'edition': '1',
            'number_of_pages': 48,
            'purchase_price': 15.0,
            'year_of_purchase': 2023,
            'place_of_purchase': 'Test Store',
            'synopsis': 'Test Synopsis',
            'image': 'test.jpg',
            'deluxe_edition': True,
        }
        BD.objects.create(**test_data)

        # Act
        result = self.repository.page(1234)

        # Assert
        self.assertIsNotNone(result)
        # Vérifie que tous les champs attendus sont présents
        self.assertEqual(self.EXPECTED_FIELDS, set(result.keys()))
        # Vérifie que le prix a été converti en entier
        self.assertEqual(15, result['purchase_price'])
        # Vérifie que tous les autres champs correspondent
        for field in self.EXPECTED_FIELDS - {'purchase_price'}:
            self.assertEqual(test_data[field], result[field])

    def test_page_with_existing_bd_decimal_price(self) -> None:
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
        BD.objects.create(**test_data)

        # Act
        result = self.repository.page(5678)

        # Assert
        self.assertIsNotNone(result)
        # Vérifie que le prix est resté décimal
        self.assertEqual(15.99, result['purchase_price'])
        # Vérifie tous les autres champs
        for field in self.EXPECTED_FIELDS - {'purchase_price'}:
            self.assertEqual(test_data[field], result[field])

    def test_page_with_null_fields(self) -> None:
        # Arrange
        test_data = {
            'isbn': 9012,
            'album': 'Test Album',
            'deluxe_edition': False,
        }

        BD.objects.create(**test_data)

        # Act
        result = self.repository.page(9012)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(self.EXPECTED_FIELDS, set(result.keys()))
        for field in self.EXPECTED_FIELDS:
            if field in ['isbn', 'album', 'deluxe_edition']:
                self.assertEqual(test_data[field], result[field])
            else:
                self.assertIn(result[field], [None, ''])

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
            BD.objects.create(**data)

        # Act & Assert
        for test_data in test_data_list:
            result = self.repository.page(int(test_data['isbn']))
            self.assertIsNotNone(result)
            self.assertEqual(test_data['album'], result['album'])
            self.assertEqual(test_data['isbn'], result['isbn'])
            if test_data['purchase_price'].is_integer():
                self.assertEqual(int(test_data['purchase_price']), result['purchase_price'])
            else:
                self.assertEqual(test_data['purchase_price'], result['purchase_price'])


if __name__ == '__main__':
    unittest.main()
