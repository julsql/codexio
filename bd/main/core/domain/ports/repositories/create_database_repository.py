from abc import abstractmethod, ABC

from main.core.domain.model.app_user import AppUser as INTERNAL_MODEL_APPUSER
from main.core.domain.model.bd import BD as INTERNAL_MODEL_BD
from main.core.domain.model.collection import Collection as INTERNAL_MODEL_COLLECTION
from main.core.infrastructure.persistence.database.models.bd import BD as DATABASE_MODEL_BD
from main.core.infrastructure.persistence.database.models.collection import Collection as DATABASE_MODEL_COLLECTION
from main.models import AppUser as DATABASE_MODEL_APPUSER


class CreateDatabaseRepository(ABC):

    @abstractmethod
    def create(self,
               value: INTERNAL_MODEL_BD | INTERNAL_MODEL_COLLECTION | INTERNAL_MODEL_APPUSER) -> DATABASE_MODEL_BD | DATABASE_MODEL_COLLECTION | DATABASE_MODEL_APPUSER:
        pass
