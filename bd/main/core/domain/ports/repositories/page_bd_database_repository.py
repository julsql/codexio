from abc import ABC, abstractmethod
from typing import Optional

from main.core.domain.model.bd import BD
from main.core.infrastructure.persistence.database.models import Collection


class WorkDatabaseRepository(ABC):
    @abstractmethod
    def page(self, isbn: int, collection: Collection) -> Optional[BD]:
        pass
