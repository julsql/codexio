from abc import ABC, abstractmethod
from typing import Any


class PageBdDatabaseRepository(ABC):
    @abstractmethod
    def page(self, isbn: int) -> dict[str, Any] | None:
        pass
