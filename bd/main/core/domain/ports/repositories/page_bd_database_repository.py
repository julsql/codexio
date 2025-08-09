from abc import ABC, abstractmethod
from typing import Optional

from main.core.domain.model.bd import BD
from main.core.domain.model.book import Book


class WorkDatabaseRepository(ABC):
    @abstractmethod
    def page(self, isbn: int, collection_id: int) -> Optional[BD | Book]:
        pass
