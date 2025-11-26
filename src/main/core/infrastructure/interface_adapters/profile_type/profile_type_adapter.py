from django.http import HttpResponseServerError

from main.core.domain.model.profile_type import ProfileType
from main.core.domain.ports.repositories.profile_repository import ProfileTypeRepository
from main.core.domain.ports.repositories.response_repository import ResponseRepository
from main.core.infrastructure.persistence.database.models import Collection


class ProfileTypeAdapter(ProfileTypeRepository):
    def __init__(self, response_adapter: ResponseRepository):
        self.response_adapter = response_adapter

    def get_profile_type(self, collection: Collection) -> ProfileType | HttpResponseServerError:
        if collection.profile.name == "BD":
            return ProfileType.BD
        elif collection.profile.name == "BOOK":
            return ProfileType.BOOK
        else:
            return self.response_adapter.technical_error("Le profil n'est pas défini ou n'existe pas")
