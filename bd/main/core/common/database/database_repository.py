from abc import abstractmethod, ABC
from typing import List


class DatabaseRepository(ABC):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def create_table(self, table_name: str, column_names: List[str]) -> None:
        pass

    @abstractmethod
    def insert(self, table_name: str, column_names: List[str], value: List[List[str]]) -> None:
        pass
