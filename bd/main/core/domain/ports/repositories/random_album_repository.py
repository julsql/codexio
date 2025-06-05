from abc import ABC, abstractmethod

from main.core.domain.model.album import Album


class RandomAlbumRepository(ABC):
    @abstractmethod
    def get_random_album(self) -> Album:
        pass
