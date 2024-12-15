from abc import abstractmethod, ABC
from typing import List, Dict, Any


class DatabaseRepository(ABC):

    @abstractmethod
    def create_table(self) -> None:
        pass

    @abstractmethod
    def insert(self,value: List[Dict[str, str]]) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Dict[str, str]]:
        pass
