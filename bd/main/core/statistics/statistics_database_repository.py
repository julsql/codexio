from abc import ABC, abstractmethod


class StatisticsDatabaseRepository(ABC):
    @abstractmethod
    def get_information(self):
        pass
