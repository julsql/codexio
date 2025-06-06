from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.bd import BD


class PageBdDatabaseRepository(ABC):
    @abstractmethod
    def page(self, isbn: int, user: AbstractBaseUser) -> Optional[BD]:
        pass
