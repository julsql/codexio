import os
import sys
import unittest
from datetime import date

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.common.database.internal.bd_model import BD
from main.core.statistics.internal.statistics_database_connexion import StatisticsDatabaseConnexion


class TestStatisticsDatabaseConnexion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repository = StatisticsDatabaseConnexion()

    def tearDown(self):
        BD.objects.all().delete()

    def test_get_information_empty_database(self) -> None:
        # Act
        result = self.repository.get_information()

        # Assert
        self.assertIsInstance(result, dict)
        expected = {
            'nombre': 0,
            'pages': 0,
            'prix': 0,
            'tirage': 0,
        }
        self.assertEqual(expected, result)

    def test_get_information_with_data(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Standard BD",
            rating=10.0,
            number_of_pages=48,
            deluxe_edition=False,
            publication_date=date(2024, 1, 1)
        )
        BD.objects.create(
            isbn="987654321",
            album="Deluxe BD",
            rating=20.0,
            number_of_pages=72,
            deluxe_edition=True,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_information()

        # Assert
        expected = {
            'nombre': 2,
            'pages': 120,
            'prix': 30,
            'tirage': 1,
        }
        self.assertEqual(expected, result)

    def test_get_information_all_deluxe(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Deluxe 1",
            deluxe_edition=True,
            rating=15.0,
            number_of_pages=60,
            publication_date=date(2024, 1, 1)
        )
        BD.objects.create(
            isbn="987654321",
            album="Deluxe 2",
            deluxe_edition=True,
            rating=25.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_information()

        # Assert
        expected = {
            'nombre': 2,
            'pages': 140,
            'prix': 40,
            'tirage': 2,
        }
        self.assertEqual(expected, result)

    def test_get_information_with_null_values(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Test BD",
            deluxe_edition=False,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_information()

        # Assert
        expected = {
            'nombre': 1,
            'pages': 0,
            'prix': 0,
            'tirage': 0,
        }
        self.assertEqual(expected, result)

    def test_get_information_with_integer_prices(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Test BD",
            rating=15,
            number_of_pages=48,
            deluxe_edition=False,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_information()

        # Assert
        self.assertEqual(15.0, result['prix'])


if __name__ == '__main__':
    unittest.main()
