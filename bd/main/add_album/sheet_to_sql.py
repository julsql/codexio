import sqlite3
import os
from sheet_connection import Conn

__FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
__DATABASE__ = os.path.join(__FILEPATH__, "comics.sqlite3")


# Fonction pour créer la table dans la base de données SQL
def create_sql_table(connection, gsheet, table_name):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (isbn BIGINT)")

    # Récupérer la première ligne de la feuille de calcul comme des colonnes de la table
    columns = gsheet.get_line(0)
    for column in columns[1:]:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN \"{column}\" TEXT")
    connection.commit()


# Fonction pour insérer les données de la feuille de calcul dans la table SQL
def insert_data_into_sql_table(connection, gsheet, table_name):
    cursor = connection.cursor()
    rows = gsheet.get_all()

    title = [f'"{titre}"' for titre in rows[0]]
    data = rows[1:]

    for row in data:
        cursor.execute(f"INSERT INTO {table_name} ({','.join(title)}) VALUES ({','.join(['?'] * len(title))})", row)

    connection.commit()


gsheet = Conn()
gsheet.open("config")

database = sqlite3.connect(__DATABASE__)

create_sql_table(database, gsheet, 'BD')
insert_data_into_sql_table(database, gsheet, 'BD')

database.close()
