from abc import ABC
from typing import Any, Optional

from main.core.random_album.random_album_repository import RandomAlbumRepository


class RandomAlbumInMemory(RandomAlbumRepository, ABC):
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.database: list[dict[str, Any]] = data
        self.get_random_album_called = False

    def get_random_album(self) -> Optional[dict[str, Any]]:
        self.get_random_album_called = True
        if not self.database:
            return None
        return self.database[0]
