from main.core.common.database.database_repository import DatabaseRepository
from main.core.common.sheet.sheet_repository import SheetRepository

class UpdateDatabaseService:
    def __init__(self, sheet_repository: SheetRepository, database_repository: DatabaseRepository) -> None:
        doc_name = "bd"
        sheet_name = "BD"
        self.sheet = sheet_repository
        self.sheet.open(doc_name, sheet_name)
        self.database = database_repository
        self.database.open()

    def main(self) -> None:
        rows = self.sheet.get_all()
        title = [f"{titre}" for titre in rows[0]]
        data = rows[1:]

        table_name = "BD"

        self.database.create_table(table_name, title)
        print(title)
        self.database.insert(table_name, title, data)
        self.database.close()
