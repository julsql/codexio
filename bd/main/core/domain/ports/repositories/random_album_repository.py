from abc import ABC, abstractmethod
from typing import Optional

from main.core.domain.model.album import Album
from main.core.infrastructure.persistence.database.models import Collection


class RandomAlbumRepository(ABC):
    @abstractmethod
    def get_random_album(self, collection: Collection) -> Optional[Album]:
        pass
