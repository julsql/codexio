import os
import sys
import unittest
from datetime import date

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.domain.model.statistics import Statistics
from main.core.infrastructure.persistence.database.models.bd import BD
from main.core.infrastructure.persistence.database.statistics_bd_database_adapter import StatisticsBdDatabaseAdapter
from main.models import AppUser
from main.core.infrastructure.persistence.database.models.collection import Collection


class TestStatisticsDatabaseConnexion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=user)
        cls.collection_id = cls.collection.id
        cls.repository = StatisticsBdDatabaseAdapter()
        BD.objects.filter(collection=cls.collection).delete()

    def tearDown(self):
        BD.objects.filter(collection=self.collection).delete()

    def test_get_information_empty_database(self) -> None:
        # Act
        result = self.repository.get_database_statistics(self.collection_id)

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
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="987654321",
            album="Deluxe BD2",
            rating=20.0,
            number_of_pages=72,
            deluxe_edition=True,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )

        # Act
        result = self.repository.get_database_statistics(self.collection_id)

        # Assert
        expected = Statistics(albums_count=2,
                              pages_count=120,
                              purchase_price_count=30,
                              deluxe_edition_count=1,
                              signed_copies_count=0,
                              ex_libris_count=0,
                              place_of_purchase_pie=[('Lyon', 2)])
        self.assertEqual(expected, result)

    def test_get_information_all_deluxe(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Deluxe 1",
            deluxe_edition=True,
            rating=15.0,
            number_of_pages=60,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="987654321",
            album="Deluxe 2",
            deluxe_edition=True,
            rating=25.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )

        # Act
        result = self.repository.get_database_statistics(self.collection_id)

        # Assert
        expected = Statistics(albums_count=2,
                              pages_count=140,
                              purchase_price_count=40,
                              deluxe_edition_count=2,
                              signed_copies_count=0,
                              ex_libris_count=0,
                              place_of_purchase_pie=[('Lyon', 2)])
        self.assertEqual(expected, result)

    def test_get_information_all_pruchase_price(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Deluxe 1",
            deluxe_edition=True,
            rating=15.0,
            number_of_pages=60,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="987654321",
            album="Deluxe 2",
            deluxe_edition=True,
            rating=25.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Paris",
            collection=self.collection,
        )

        # Act
        result = self.repository.get_database_statistics(self.collection_id)

        # Assert
        expected = Statistics(albums_count=2,
                              pages_count=140,
                              purchase_price_count=40,
                              deluxe_edition_count=2,
                              signed_copies_count=0,
                              ex_libris_count=0,
                              place_of_purchase_pie=[("Lyon", 1), ('Paris', 1)])
        self.assertEqual(expected, result)

    def test_get_information_all_multiple_pruchase_price(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Deluxe 1",
            deluxe_edition=True,
            rating=15.0,
            number_of_pages=60,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456788",
            album="Deluxe 2",
            deluxe_edition=True,
            rating=15.0,
            number_of_pages=60,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456787",
            album="Deluxe 3",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Paris",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456786",
            album="Deluxe 4",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Paris",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456785",
            album="Deluxe 5",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Le Mans",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456784",
            album="Deluxe 6",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Le Mans",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456783",
            album="Deluxe 7",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Bordeaux",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456782",
            album="Deluxe 8",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Bordeaux",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="123456781",
            album="Deluxe 9",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Marseille",
            collection=self.collection,
        )
        BD.objects.create(
            isbn="1234567880",
            album="Deluxe 10",
            deluxe_edition=False,
            rating=15.0,
            number_of_pages=80,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Toulouse",
            collection=self.collection,
        )

        # Act
        result = self.repository.get_database_statistics(self.collection_id)

        # Assert
        expected = Statistics(albums_count=10,
                              pages_count=760,
                              purchase_price_count=150,
                              deluxe_edition_count=2,
                              signed_copies_count=0,
                              ex_libris_count=0,
                              place_of_purchase_pie=[("Bordeaux", 2),
                                                     ('Le Mans', 2),
                                                     ('Lyon', 2),
                                                     ('Paris', 2),
                                                     ('AUTRE', 2),
                                                     ])
        self.assertEqual(expected, result)

    def test_get_information_with_null_values(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Test BD2",
            deluxe_edition=False,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )

        # Act
        result = self.repository.get_database_statistics(self.collection_id)

        # Assert
        expected = Statistics(albums_count=1,
                              pages_count=0,
                              purchase_price_count=0,
                              deluxe_edition_count=0,
                              signed_copies_count=0,
                              ex_libris_count=0,
                              place_of_purchase_pie=[('Lyon', 1)])

        self.assertEqual(expected, result)

    def test_get_information_with_integer_prices(self) -> None:
        # Arrange
        BD.objects.create(
            isbn="123456789",
            album="Test BD2",
            rating=15,
            number_of_pages=48,
            deluxe_edition=False,
            publication_date=date(2024, 1, 1),
            place_of_purchase="Lyon",
            collection=self.collection,
        )

        # Act
        result = self.repository.get_database_statistics(self.collection_id)

        # Assert
        self.assertEqual(15.0, result.purchase_price_count)


if __name__ == '__main__':
    unittest.main()
