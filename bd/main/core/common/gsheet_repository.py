from abc import ABC, abstractmethod

class GsheetRepository(ABC):
    @abstractmethod
    def open(self, doc_name: str, sheet_name: str = None):
        pass

    @abstractmethod
    def append(self, liste: list):
        pass

    @abstractmethod
    def get(self, i: int, j: int) -> str:
        pass

    @abstractmethod
    def get_line(self, i: int) -> list:
        pass

    @abstractmethod
    def get_column(self, j: int) -> list:
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def set(self, valeur: str, i: int, j: int):
        pass

    @abstractmethod
    def set_line(self, valeur: list, i: int):
        pass

    @abstractmethod
    def set_column(self, valeur: str, j: int):
        pass

    @abstractmethod
    def delete_row(self, i: int):
        pass

    @abstractmethod
    def double(self, isbn: int) -> bool:
        pass

