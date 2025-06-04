from abc import ABC, abstractmethod
from typing import Optional

from main.domain.model.bd import BD


class PageBdDatabaseRepository(ABC):
    @abstractmethod
    def page(self, isbn: int) -> Optional[BD]:
        pass
