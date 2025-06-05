from abc import abstractmethod, ABC

from main.core.domain.model.bd import BD


class DatabaseRepository(ABC):

    @abstractmethod
    def reset_table(self) -> None:
        pass

    @abstractmethod
    def insert(self, value: list[BD]) -> None:
        pass
