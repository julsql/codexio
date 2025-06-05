from abc import ABC, abstractmethod

from main.core.domain.model.album import Album


class AlbumRepository(ABC):
    @abstractmethod
    def get_infos(self, isbn: int) -> Album:
        pass

    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_html(self, url: str) -> str:
        pass
