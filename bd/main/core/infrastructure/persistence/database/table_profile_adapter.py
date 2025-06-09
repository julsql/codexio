from main.core.domain.model.profile import Profile as INTERNAL_MODEL_PROFILE
from main.core.domain.ports.repositories.create_database_repository import CreateDatabaseRepository
from main.core.infrastructure.persistence.database.models.profile import Profile as DATABASE_MODEL_PROFILE


class TableProfileAdapter(CreateDatabaseRepository):
    def create(self,
               value: INTERNAL_MODEL_PROFILE) -> DATABASE_MODEL_PROFILE:
        user = DATABASE_MODEL_PROFILE.objects.create(name=value.name)
        user.save()
        return user
