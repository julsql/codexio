import sqlite3
from typing import List

from main.core.common.database.database_repository import DatabaseRepository


class DatabaseConnexion(DatabaseRepository):
    def __init__(self):
        self.database = None

    def open(self, file: str):
        self.database = sqlite3.connect(file)

    def close(self):
        self.database.close()

    def create_table(self, table_name: str, column_names: List[str]) -> None:
        cursor = self.database.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"CREATE TABLE {table_name} (isbn BIGINT)")

        for column_name in column_names[1:]:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT")
        self.database.commit()

    def insert(self, table_name: str, column_names: List[str], value: List[List[str]]) -> None:
        cursor = self.database.cursor()

        for row in value:
            cursor.execute(f"INSERT INTO {table_name} ({','.join(column_names)}) VALUES ({','.join(['?'] * len(column_names))})", row)

        self.database.commit()
