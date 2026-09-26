from typing import Optional

from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.album_cache_repository import AlbumCacheRepository


class AlbumCacheInMemory(AlbumCacheRepository):
    def __init__(self) -> None:
        self.entries: dict[tuple[str, int], Album] = {}
        self.reads = 0
        self.writes = 0

    def get(self, source: str, isbn: int) -> Optional[Album]:
        self.reads += 1
        return self.entries.get((source, isbn))

    def save(self, source: str, isbn: int, album: Album) -> None:
        self.writes += 1
        self.entries[(source, isbn)] = album
