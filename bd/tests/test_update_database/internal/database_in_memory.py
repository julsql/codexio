from typing import List, Dict

from main.core.common.database.database_repository import DatabaseRepository


class DatabaseInMemory(DatabaseRepository):
    def __init__(self, filename: str):
        self.filename = filename
        self.database = []
        self.column_names = None

    def create_table(self) -> None:
        self.database = []

    def insert(self, value: List[Dict[str, str]]) -> None:
        self.database = value

    def get_all(self):
        return self.database
