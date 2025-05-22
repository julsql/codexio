import unittest

from main.application.usecases.statistics.statistics_service import StatisticsService
from main.domain.model.statistics import Statistics
from test_statistics.internal.statistics_attachments_in_memory import StatisticsAttachmentsInMemory
from test_statistics.internal.statistics_database_in_memory import StatisticsDatabaseInMemory


class TestStatisticsService(unittest.TestCase):
    def setUp(self) -> None:
        self.statistics = Statistics(
            nombre_albums=100,
            nombre_pages=20,
            prix_total=80,
            nombre_editions_speciales=80,
            nombre_dedicaces=30,
            nombre_exlibris=15,
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
        expected.nombre_dedicaces = self.statistics.nombre_dedicaces
        expected.nombre_exlibris = self.statistics.nombre_exlibris
        self.assertEqual(expected, result)

    def test_main_with_empty_attachments_info(self) -> None:
        # Arrange
        attachments_repository = StatisticsAttachmentsInMemory(Statistics.empty())

        # Act
        service = StatisticsService(self.database_repository, attachments_repository)
        result = service.execute()

        # Assert
        expected = Statistics.empty()
        expected.nombre_albums = self.statistics.nombre_albums
        expected.nombre_pages = self.statistics.nombre_pages
        expected.prix_total = self.statistics.prix_total
        expected.nombre_editions_speciales = self.statistics.nombre_editions_speciales
        self.assertEqual(expected, result)

    def test_main_with_overlapping_keys(self) -> None:
        # Arrange
        database_info = Statistics(
            nombre_albums=100,
            nombre_pages=20,
            prix_total=80,
            nombre_editions_speciales=80,
            nombre_dedicaces=200,
            nombre_exlibris=200,
        )
        attachments_info = Statistics(
            nombre_albums=200,
            nombre_pages=200,
            prix_total=200,
            nombre_editions_speciales=200,
            nombre_dedicaces=30,
            nombre_exlibris=15,
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
