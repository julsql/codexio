from abc import ABC, abstractmethod

from main.core.domain.model.statistics import Statistics


class StatisticsDatabaseRepository(ABC):
    @abstractmethod
    def get_database_statistics(self) -> Statistics:
        pass
