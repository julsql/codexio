from abc import ABC, abstractmethod
from typing import Optional

from main.core.domain.model.album import Album


class AlbumCacheRepository(ABC):
    @abstractmethod
    def get(self, source: str, isbn: int) -> Optional[Album]:
        """Renvoie la notice mémorisée pour cette source, ou None si absente ou périmée"""
        pass

    @abstractmethod
    def save(self, source: str, isbn: int, album: Album) -> None:
        """Mémorise la notice renvoyée par cette source"""
        pass
