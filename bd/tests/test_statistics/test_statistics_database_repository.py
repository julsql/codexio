import os
import sys
import unittest
from datetime import date

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.domain.model.statistics import Statistics
from main.infrastructure.persistence.database.models import BD
from main.infrastructure.persistence.database.statistics_database_adapter import StatisticsDatabaseAdapter


class TestStatisticsDatabaseConnexion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repository = StatisticsDatabaseAdapter()
        BD.objects.all().delete()

    def tearDown(self):
        BD.objects.all().delete()

    def test_get_information_empty_database(self) -> None:
        # Act
        result = self.repository.get_database_statistics()

        # Assert
        self.assertIsInstance(result, Statistics)
        expected = Statistics.empty()
        self.assertEqual(expected, result)

    def test_get_information_with_data(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Standard BD2",
            rating=10.0,
            number_of_pages=48,
            deluxe_edition=False,
            publication_date=date(2024, 1, 1)
        )
        BD.objects.create(
            isbn="987654321",
            album="Deluxe BD2",
            rating=20.0,
            number_of_pages=72,
            deluxe_edition=True,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_database_statistics()

        # Assert
        expected = Statistics(nombre_albums=2,
                              nombre_pages=120,
                              prix_total=30,
                              nombre_editions_speciales=1,
                              nombre_dedicaces=0,
                              nombre_exlibris=0)
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
        result = self.repository.get_database_statistics()

        # Assert
        expected = Statistics(nombre_albums=2,
                              nombre_pages=140,
                              prix_total=40,
                              nombre_editions_speciales=2,
                              nombre_dedicaces=0,
                              nombre_exlibris=0)
        self.assertEqual(expected, result)

    def test_get_information_with_null_values(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Test BD2",
            deluxe_edition=False,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_database_statistics()

        # Assert
        expected = Statistics(nombre_albums=1,
                              nombre_pages=0,
                              prix_total=0,
                              nombre_editions_speciales=0,
                              nombre_dedicaces=0,
                              nombre_exlibris=0)

        self.assertEqual(expected, result)

    def test_get_information_with_integer_prices(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Test BD2",
            rating=15,
            number_of_pages=48,
            deluxe_edition=False,
            publication_date=date(2024, 1, 1)
        )

        # Act
        result = self.repository.get_database_statistics()

        # Assert
        self.assertEqual(15.0, result.prix_total)


if __name__ == '__main__':
    unittest.main()
