from abc import abstractmethod, ABC

from main.core.domain.model.bd import BD
from main.core.infrastructure.persistence.database.models import Collection


class DatabaseRepository(ABC):

    @abstractmethod
    def reset_table(self, collection_id: int) -> None:
        pass

    @abstractmethod
    def insert(self, value: list[BD], collection: Collection) -> None:
        pass
