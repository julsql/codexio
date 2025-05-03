import unittest

from main.core.statistics.statistics_service import StatisticsService
from test_statistics.internal.statistics_attachments_in_memory import StatisticsAttachmentsInMemory
from test_statistics.internal.statistics_database_in_memory import StatisticsDatabaseInMemory


class TestStatisticsService(unittest.TestCase):
    def setUp(self) -> None:
        self.database_info = {
            "total": 100,
            "deluxe": 20,
            "standard": 80
        }
        self.attachments_info = {
            "dedicaces": 30,
            "exlibris": 15
        }

        self.attachments_repository = StatisticsAttachmentsInMemory(self.attachments_info)
        self.database_repository = StatisticsDatabaseInMemory(self.database_info)
        self.service = StatisticsService(self.attachments_repository, self.database_repository)

    def test_main_calls_both_repositories(self) -> None:
        # Act
        self.service.main()

        # Assert
        self.assertTrue(self.attachments_repository.get_information_called)
        self.assertTrue(self.database_repository.get_information_called)

    def test_main_merges_repository_results(self) -> None:
        # Act
        result = self.service.main()

        # Assert
        expected = {**self.database_info, **self.attachments_info}
        self.assertEqual(expected, result)

    def test_main_with_empty_database_info(self) -> None:
        # Arrange
        self.database_repository = StatisticsDatabaseInMemory({})

        # Act
        service = StatisticsService(self.attachments_repository, self.database_repository)
        result = service.main()

        # Assert
        self.assertEqual(self.attachments_info, result)

    def test_main_with_empty_attachments_info(self) -> None:
        # Arrange
        self.attachments_repository = StatisticsAttachmentsInMemory({})

        # Act
        service = StatisticsService(self.attachments_repository, self.database_repository)
        result = service.main()

        # Assert
        self.assertEqual(self.database_info, result)

    def test_main_with_overlapping_keys(self) -> None:
        # Arrange
        database_info = {"total": 100, "common": "db_value"}
        attachments_info = {"dedicaces": 30, "common": "att_value"}

        database_repository = StatisticsDatabaseInMemory(database_info)
        attachments_repository = StatisticsAttachmentsInMemory(attachments_info)
        service = StatisticsService(attachments_repository, database_repository)

        # Act
        result = service.main()

        # Assert
        self.assertEqual("att_value", result["common"])
        self.assertEqual(100, result["total"])
        self.assertEqual(30, result["dedicaces"])

    def test_main_with_empty_repositories(self) -> None:
        # Arrange
        database_repository = StatisticsDatabaseInMemory({})
        attachments_repository = StatisticsAttachmentsInMemory({})
        service = StatisticsService(attachments_repository, database_repository)

        # Act
        result = service.main()

        # Assert
        self.assertEqual({}, result)


if __name__ == '__main__':
    unittest.main()
