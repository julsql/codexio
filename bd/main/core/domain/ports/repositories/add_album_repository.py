from abc import ABC, abstractmethod

from main.core.domain.model.album import Album
from main.core.domain.model.book import Book


class AddAlbumRepository(ABC):
    @abstractmethod
    def get_infos(self, isbn: int) -> Album | Book:
        pass
