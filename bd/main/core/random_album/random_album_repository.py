from abc import ABC, abstractmethod
from typing import Any


class RandomAlbumRepository(ABC):
    @abstractmethod
    def get_random_album(self) -> dict[str, Any] | None:
        pass
