from main.core.application.usecases.update_database.update_database_service import UpdateDatabaseService
from main.core.infrastructure.persistence.database.table_bd_adapter import TableBdAdapter
from main.core.infrastructure.persistence.sheet.sheet_adapter import SheetAdapter
from main.models import AppUser


def insert_initial_data() -> None:
    users = AppUser.objects.exclude(username='admin').filter(is_active=True)
    for user in users:
        for collection in user.collections.all():
            sheet_repository = SheetAdapter(collection.doc_id, collection.sheet_name)
            database_repository = TableBdAdapter()
            service = UpdateDatabaseService(sheet_repository, database_repository)
            service.main(collection)

if __name__ == '__main__':
    insert_initial_data()
