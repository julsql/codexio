from abc import ABC, abstractmethod

from django.http import HttpResponseServerError

from main.core.domain.model.profile_type import ProfileType
from main.core.infrastructure.persistence.database.models import Collection


class ProfileTypeRepository(ABC):
    @abstractmethod
    def get_profile_type(self, collection: Collection) -> ProfileType | HttpResponseServerError:
        pass
