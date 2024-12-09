from abc import abstractmethod, ABC
from typing import List, Dict, Any


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

    @abstractmethod
    def get_all(self, table_name: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_one(self, query: str) -> Dict[str, Any]:
        pass
