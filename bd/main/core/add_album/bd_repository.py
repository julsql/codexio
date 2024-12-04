from abc import ABC, abstractmethod
from typing import Dict

class BdRepository(ABC):
    @abstractmethod
    def get_infos(self, isbn: int) -> Dict:
        pass

    @abstractmethod
    def get_url(self, isbn: int) -> str:
        pass
