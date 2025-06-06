from abc import ABC, abstractmethod
from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import QuerySet

from main.core.infrastructure.persistence.database.models.bd import BD


class AdvancedSearchRepository(ABC):
    @abstractmethod
    def get_all(self, user: AbstractBaseUser) -> QuerySet[BD, BD]:
        pass

    @abstractmethod
    def get_by_form(self, data: dict[str, Any], queryset: QuerySet[BD, BD]) -> QuerySet[BD, BD]:
        pass
