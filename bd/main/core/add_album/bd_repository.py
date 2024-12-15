from abc import ABC, abstractmethod


class BdRepository(ABC):
    @abstractmethod
    def get_infos(self, isbn: int) -> dict[str, str | float | int]:
        pass

    @abstractmethod
    def get_url(self, isbn: int) -> str:
        pass
