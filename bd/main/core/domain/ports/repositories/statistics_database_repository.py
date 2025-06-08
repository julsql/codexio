from abc import ABC, abstractmethod

from main.core.domain.model.statistics import Statistics
from main.core.infrastructure.persistence.database.models import Collection


class StatisticsDatabaseRepository(ABC):
    @abstractmethod
    def get_database_statistics(self, collection: Collection) -> Statistics:
        pass
