import unittest

from main.application.usecases.statistics.statistics_service import StatisticsService
from main.domain.model.statistics import Statistics
from test_statistics.internal.statistics_attachments_in_memory import StatisticsAttachmentsInMemory
from test_statistics.internal.statistics_database_in_memory import StatisticsDatabaseInMemory


class TestStatisticsService(unittest.TestCase):
    def setUp(self) -> None:
        self.statistics = Statistics(
            albums_count=100,
            pages_count=20,
            purchase_price_count=80,
            deluxe_edition_count=80,
            signed_copies_count=30,
            ex_libris_count=15,
        )

        self.attachments_repository = StatisticsAttachmentsInMemory(self.statistics)
        self.database_repository = StatisticsDatabaseInMemory(self.statistics)
        self.service = StatisticsService(self.database_repository, self.attachments_repository)

    def test_main_calls_both_repositories(self) -> None:
        # Act
        self.service.execute()

        # Assert
        self.assertTrue(self.attachments_repository.get_information_called)
        self.assertTrue(self.database_repository.get_information_called)

    def test_main_merges_repository_results(self) -> None:
        # Act
        result = self.service.execute()

        # Assert
        expected = self.statistics
        self.assertEqual(expected, result)

    def test_main_with_empty_database_info(self) -> None:
        # Arrange
        database_repository = StatisticsDatabaseInMemory(Statistics.empty())

        # Act
        service = StatisticsService(database_repository, self.attachments_repository)
        result = service.execute()

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
        result = service.execute()

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
        )
        attachments_info = Statistics(
            albums_count=200,
            pages_count=200,
            purchase_price_count=200,
            deluxe_edition_count=200,
            signed_copies_count=30,
            ex_libris_count=15,
        )

        database_repository = StatisticsDatabaseInMemory(database_info)
        attachments_repository = StatisticsAttachmentsInMemory(attachments_info)
        service = StatisticsService(database_repository, attachments_repository)

        # Act
        result = service.execute()

        # Assert
        self.assertEqual(self.statistics, result)

    def test_main_with_empty_repositories(self) -> None:
        # Arrange
        database_repository = StatisticsDatabaseInMemory(Statistics.empty())
        attachments_repository = StatisticsAttachmentsInMemory(Statistics.empty())
        service = StatisticsService(database_repository, attachments_repository)

        # Act
        result = service.execute()

        # Assert
        self.assertEqual(Statistics.empty(), result)


if __name__ == '__main__':
    unittest.main()
