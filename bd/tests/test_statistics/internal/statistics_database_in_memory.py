from abc import ABC

from main.core.domain import StatisticsDatabaseRepository
from main.core.domain.model.statistics import Statistics


class StatisticsDatabaseInMemory(StatisticsDatabaseRepository, ABC):
    def __init__(self, return_value: Statistics) -> None:
        self.return_value = return_value
        self.get_information_called = False

    def get_database_statistics(self) -> Statistics:
        self.get_information_called = True
        return self.return_value
