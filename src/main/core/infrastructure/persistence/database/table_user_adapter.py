from main.core.domain.model.app_user import AppUser as INTERNAL_MODEL_APPUSER
from main.core.domain.ports.repositories.create_database_repository import CreateDatabaseRepository
from main.models import AppUser as DATABASE_MODEL_APPUSER


class TableUserAdapter(CreateDatabaseRepository):
    def create(self,
               value: INTERNAL_MODEL_APPUSER) -> DATABASE_MODEL_APPUSER:
        user = DATABASE_MODEL_APPUSER.objects.create_user(username=value.username, password=value.password)
        user.first_name = value.first_name
        user.email = value.email
        user.save()
        return user
