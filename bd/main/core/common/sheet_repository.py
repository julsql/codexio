from abc import ABC, abstractmethod
from typing import List


class SheetRepository(ABC):
    @abstractmethod
    def open(self, doc_name: str, sheet_name: str = None):
        pass

    @abstractmethod
    def append(self, liste: List):
        pass

    @abstractmethod
    def get(self, i: int, j: int) -> str:
        pass

    @abstractmethod
    def get_line(self, i: int) -> List:
        pass

    @abstractmethod
    def get_column(self, j: int) -> List:
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def set(self, valeur: str, i: int, j: int):
        pass

    @abstractmethod
    def set_line(self, valeur: List, i: int):
        pass

    @abstractmethod
    def set_column(self, valeur: List, j: int):
        pass

    @abstractmethod
    def delete_row(self, i: int):
        pass

    @abstractmethod
    def double(self, isbn: int) -> bool:
        pass

