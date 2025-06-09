from abc import ABC, abstractmethod
from typing import Any

from django.db.models import QuerySet


class AdvancedSearchRepository(ABC):
    @abstractmethod
    def get_all(self, collection_id: int) -> QuerySet:
        pass

    @abstractmethod
    def get_by_form(self, data: dict[str, Any], queryset: QuerySet) -> QuerySet:
        pass
