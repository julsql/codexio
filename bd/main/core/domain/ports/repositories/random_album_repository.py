from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.album import Album


class RandomAlbumRepository(ABC):
    @abstractmethod
    def get_random_album(self, user: AbstractBaseUser) -> Optional[Album]:
        pass
