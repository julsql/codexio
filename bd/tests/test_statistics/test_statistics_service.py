import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.application.usecases.statistics.statistics_service import StatisticsService
from main.core.domain.model.statistics import Statistics
from tests.test_statistics.internal.statistics_attachments_in_memory import StatisticsAttachmentsInMemory
from tests.test_statistics.internal.statistics_database_in_memory import StatisticsDatabaseInMemory
from main.models import AppUser
from main.core.infrastructure.persistence.database.models.collection import Collection


class TestStatisticsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=cls.user)

    def setUp(self) -> None:
        self.statistics = Statistics(
            albums_count=100,
            pages_count=20,
            purchase_price_count=80,
            deluxe_edition_count=80,
            signed_copies_count=30,
            ex_libris_count=15,
            place_of_purchase_pie=[],
        )

        self.attachments_repository = StatisticsAttachmentsInMemory(self.statistics)
        self.database_repository = StatisticsDatabaseInMemory(self.statistics)
        self.service = StatisticsService(self.database_repository, self.attachments_repository)

    def test_main_calls_both_repositories(self) -> None:
        # Act
        self.service.execute(self.user)

        # Assert
        self.assertTrue(self.attachments_repository.get_information_called)
        self.assertTrue(self.database_repository.get_information_called)

    def test_main_merges_repository_results(self) -> None:
        # Act
        result = self.service.execute(self.user)

        # Assert
        expected = self.statistics
        self.assertEqual(expected, result)

    def test_main_with_empty_database_info(self) -> None:
        # Arrange
        database_repository = StatisticsDatabaseInMemory(Statistics.empty())

        # Act
        service = StatisticsService(database_repository, self.attachments_repository)
        result = service.execute(self.user)

        # Assert
        expected = Statistics.empty()
        expected.signed_copies_count = self.statistics.signed_copies_count
        expected.ex_libris_count = self.statistics.ex_libris_count
        self.assertEqual(expected, result)

    def test_main_with_empty_attachments_info(self) -> None:
        # Arrange
        attachments_repository = StatisticsAttachmentsInMemory(Statistics.empty())

        # Act
        service = StatisticsService(self.database_repository, attachments_repository)
        result = service.execute(self.user)

        # Assert
        expected = Statistics.empty()
        expected.albums_count = self.statistics.albums_count
        expected.pages_count = self.statistics.pages_count
        expected.purchase_price_count = self.statistics.purchase_price_count
        expected.deluxe_edition_count = self.statistics.deluxe_edition_count
        self.assertEqual(expected, result)

    def test_main_with_overlapping_keys(self) -> None:
        # Arrange
        database_info = Statistics(
            albums_count=100,
            pages_count=20,
            purchase_price_count=80,
            deluxe_edition_count=80,
            signed_copies_count=200,
            ex_libris_count=200,
            place_of_purchase_pie=[],
        )
        attachments_info = Statistics(
            albums_count=200,
            pages_count=200,
            purchase_price_count=200,
            deluxe_edition_count=200,
            signed_copies_count=30,
            ex_libris_count=15,
            place_of_purchase_pie=[],
        )

        database_repository = StatisticsDatabaseInMemory(database_info)
        attachments_repository = StatisticsAttachmentsInMemory(attachments_info)
        service = StatisticsService(database_repository, attachments_repository)

        # Act
        result = service.execute(self.user)

        # Assert
        self.assertEqual(self.statistics, result)

    def test_main_with_empty_repositories(self) -> None:
        # Arrange
        database_repository = StatisticsDatabaseInMemory(Statistics.empty())
        attachments_repository = StatisticsAttachmentsInMemory(Statistics.empty())
        service = StatisticsService(database_repository, attachments_repository)

        # Act
        result = service.execute(self.user)

        # Assert
        self.assertEqual(Statistics.empty(), result)


if __name__ == '__main__':
    unittest.main()
