from abc import abstractmethod, ABC

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.bd import BD
from main.models import AppUser


class DatabaseRepository(ABC):

    @abstractmethod
    def reset_table(self, user: AbstractBaseUser) -> None:
        pass

    @abstractmethod
    def insert(self, value: list[BD], user: AppUser) -> None:
        pass
