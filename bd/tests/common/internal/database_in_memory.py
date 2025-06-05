from typing import Dict

from main.core.domain import DatabaseRepository


class DatabaseInMemory(DatabaseRepository):
    def __init__(self):
        self.database = None
        self.column_names = None

    def reset_table(self) -> None:
        self.database = []

    def insert(self, value: list[Dict[str, str]]) -> None:
        self.database = value

    def get_all(self) -> list:
        return self.database
