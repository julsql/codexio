from abc import ABC

from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.random_album_repository import RandomAlbumRepository


class RandomAlbumInMemory(RandomAlbumRepository, ABC):
    def __init__(self, data: list[Album]) -> None:
        self.database: list[Album] = data
        self.get_random_album_called = False

    def get_random_album(self) -> Album:
        self.get_random_album_called = True
        if not self.database:
            return Album(0)
        return self.database[0]
