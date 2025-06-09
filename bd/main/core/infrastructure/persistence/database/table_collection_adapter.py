from main.core.domain.model.collection import Collection as INTERNAL_MODEL_COLLECTION
from main.core.domain.ports.repositories.create_database_repository import CreateDatabaseRepository
from main.core.infrastructure.persistence.database.models.collection import Collection as DATABASE_MODEL_COLLECTION


class TableCollectionAdapter(CreateDatabaseRepository):
    def create(self,
               value: INTERNAL_MODEL_COLLECTION) -> DATABASE_MODEL_COLLECTION:
        collection = DATABASE_MODEL_COLLECTION.objects.create(title=value.title,
                                                              token=value.token,
                                                              doc_name=value.doc_name,
                                                              sheet_name=value.sheet_name, )
        collection.accounts.add(*value.accounts)
        collection.save()
        return collection
