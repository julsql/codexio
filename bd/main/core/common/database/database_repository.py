from abc import abstractmethod, ABC


class DatabaseRepository(ABC):

    @abstractmethod
    def reset_table(self) -> None:
        pass

    @abstractmethod
    def insert(self, value: list[dict[str, str]]) -> None:
        pass
