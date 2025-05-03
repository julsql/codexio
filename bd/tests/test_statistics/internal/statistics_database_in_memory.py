from abc import ABC

from main.core.statistics.statistics_database_repository import StatisticsDatabaseRepository


class StatisticsDatabaseInMemory(StatisticsDatabaseRepository, ABC):
    def __init__(self, return_value: dict[str, int]) -> None:
        self.return_value = return_value
        self.get_information_called = False

    def get_information(self) -> dict[str, int]:
        self.get_information_called = True
        return self.return_value
