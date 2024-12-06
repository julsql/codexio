import sqlite3
from typing import List, Dict, Any

from main.core.common.database.database_repository import DatabaseRepository


class DatabaseConnexion(DatabaseRepository):
    def __init__(self, filename: str):
        self.filename = filename
        self.database = None

    def open(self):
        self.database = sqlite3.connect(self.filename)

    def close(self):
        self.database.close()

    def create_table(self, table_name: str, column_names: List[str]) -> None:
        if not self._is_valid_table_name(table_name):
            raise ValueError(f"Nom de table invalide : {table_name}")

        cursor = self.database.cursor()

        columns = [f'"{name}" TEXT' if i != 0 else f'"{name}" BIGINT' for i, name in enumerate(column_names)]
        columns_definition = ", ".join(columns)

        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"CREATE TABLE {table_name} ({columns_definition})")
        self.database.commit()

    def insert(self, table_name: str, column_names: List[str], value: List[List[str]]) -> None:
        column_names = [f'\"{column_name}\"' for column_name in column_names]
        if not self._is_valid_table_name(table_name):
            raise ValueError(f"Nom de table invalide : {table_name}")

        cursor = self.database.cursor()

        for row in value:
            cursor.execute(f"INSERT INTO {table_name} ({','.join(column_names)}) VALUES ({','.join(['?'] * len(column_names))})", row)

        self.database.commit()

    def get_all(self, table_name: str) -> List[Dict[str, Any]]:
        if not self._is_valid_table_name(table_name):
            raise ValueError(f"Nom de table invalide : {table_name}")

        cursor = self.database.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        columns = [description[0] for description in cursor.description]

        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def get(self, query: str) -> List[Dict[str, Any]]:
        cursor = self.database.cursor()
        cursor.execute(query)

        columns = [description[0] for description in cursor.description]

        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def get_one(self, query: str) -> Dict[str, Any]:
        cursor = self.database.cursor()
        cursor.execute(query)

        columns = [description[0] for description in cursor.description]

        row = cursor.fetchone()
        return dict(zip(columns, row))

    def _is_valid_table_name(self, table_name: str) -> bool:
        return table_name.isidentifier() and " " not in table_name
