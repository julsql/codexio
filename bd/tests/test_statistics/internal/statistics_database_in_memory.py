from abc import ABC

from main.core.domain.model.statistics import Statistics
from main.core.domain.ports.repositories.statistics_database_repository import StatisticsDatabaseRepository


class StatisticsDatabaseInMemory(StatisticsDatabaseRepository, ABC):
    def __init__(self, return_value: Statistics) -> None:
        self.return_value = return_value
        self.get_information_called = False

    def get_database_statistics(self) -> Statistics:
        self.get_information_called = True
        return self.return_value
