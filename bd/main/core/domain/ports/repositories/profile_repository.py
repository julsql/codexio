from abc import ABC, abstractmethod

from django.http import HttpResponseServerError

from main.core.domain.model.profile_type import ProfileType


class ProfileTypeRepository(ABC):
    @abstractmethod
    def get_profile_type(self, collection_id: int) -> ProfileType | HttpResponseServerError:
        pass
