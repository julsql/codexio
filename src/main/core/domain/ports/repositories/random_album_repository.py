from abc import ABC, abstractmethod
from typing import Optional

from main.core.domain.model.album import Album


class RandomAlbumRepository(ABC):
    @abstractmethod
    def get_random_album(self, collection_id: int) -> Optional[Album]:
        pass
