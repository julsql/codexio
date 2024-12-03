import sqlite3

from config.settings import DATABASES
from main.core.common.sheet_repository import SheetRepository

class UpdateDatabaseService:
    def __init__(self, sheet_repository: SheetRepository) -> None:
        doc_name = "bd"
        sheet_name = "BD"
        self.connexion = sheet_repository
        self.connexion.open(doc_name, sheet_name)
        database_file = DATABASES['default']['NAME'][0]
        self.database = sqlite3.connect(database_file)

    def main(self) -> None:
        rows = self.connexion.get_all()

        title = [f'"{titre}"' for titre in rows[0]]
        data = rows[1:]

        table_name = "BD"

        self.create_sql_table(title, table_name)
        self.insert_data_into_sql_table(title, data, table_name)

        self.database.close()

    def create_sql_table(self, titles, table_name):
        cursor = self.database.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"CREATE TABLE {table_name} (isbn BIGINT)")

        # Récupérer la première ligne de la feuille de calcul comme des colonnes de la table
        for title in titles[1:]:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {title} TEXT")
        self.database.commit()

    def insert_data_into_sql_table(self, title, data, table_name):
        cursor = self.database.cursor()

        for row in data:
            cursor.execute(f"INSERT INTO {table_name} ({','.join(title)}) VALUES ({','.join(['?'] * len(title))})", row)

        self.database.commit()
