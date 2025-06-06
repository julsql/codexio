from main.core.domain.model.collection import Collection as INTERNAL_MODEL_COLLECTION
from main.core.domain.ports.repositories.create_database_repository import CreateDatabaseRepository
from main.core.infrastructure.persistence.database.models.collection import Collection as DATABASE_MODEL_COLLECTION


class TableCollectionAdapter(CreateDatabaseRepository):
    def create(self,
               value: INTERNAL_MODEL_COLLECTION) -> DATABASE_MODEL_COLLECTION:
        collection = DATABASE_MODEL_COLLECTION.objects.create(title=value.title)
        collection.accounts.add(*value.accounts)
        collection.save()
        return collection
