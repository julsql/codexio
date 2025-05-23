from abc import ABC, abstractmethod
from typing import Any

from django.db.models import QuerySet

from main.infrastructure.persistence.database.models import BD


class AdvancedSearchRepository(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet[BD, BD]:
        pass

    @abstractmethod
    def get_by_form(self, data: dict[str, Any], queryset: QuerySet[BD, BD]) -> QuerySet[BD, BD]:
        pass
