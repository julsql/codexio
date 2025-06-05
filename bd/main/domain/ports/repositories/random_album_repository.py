from abc import ABC, abstractmethod

from main.domain.model.album import Album


class RandomAlbumRepository(ABC):
    @abstractmethod
    def get_random_album(self) -> Album:
        pass
