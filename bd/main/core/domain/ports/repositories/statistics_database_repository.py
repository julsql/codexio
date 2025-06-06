from abc import ABC, abstractmethod

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.statistics import Statistics


class StatisticsDatabaseRepository(ABC):
    @abstractmethod
    def get_database_statistics(self, user: AbstractBaseUser) -> Statistics:
        pass
