import gspread
from google.auth import exceptions
from google.oauth2 import service_account
import os
import sqlite3
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Niveau minimal des messages enregistrés
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format des messages
    datefmt='%Y-%m-%d %H:%M:%S'  # Format de la date
)

__FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
__DATABASE__ = os.path.join(os.path.dirname(__FILEPATH__), 'db', 'db.sqlite3')
credentials_path = os.path.join(__FILEPATH__, 'private/bd-sheet-91.json')


# Fonction pour créer la table dans la base de données SQL
def create_sql_table(connection, titles, table_name):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"CREATE TABLE {table_name} (isbn BIGINT)")

    # Récupérer la première ligne de la feuille de calcul comme des colonnes de la table
    for title in titles[1:]:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {title} TEXT")
    connection.commit()


# Fonction pour insérer les données de la feuille de calcul dans la table SQL
def insert_data_into_sql_table(connection, title, data, table_name):
    cursor = connection.cursor()

    for row in data:
        cursor.execute(f"INSERT INTO {table_name} ({','.join(title)}) VALUES ({','.join(['?'] * len(title))})", row)

    connection.commit()


def get_line(worksheet, i):
    return worksheet.row_values(i + 1)


def get_all(worksheet):
    return worksheet.get_all_values()


def update():
    try:
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.Client(auth=creds)
        client.login()
    except exceptions.DefaultCredentialsError:
        message_log = "Google Sheet non accessible."
        logging.error(message_log)
        return None

    worksheet = client.open("bd").sheet1

    database = sqlite3.connect(__DATABASE__)

    rows = get_all(worksheet)

    title = [f'"{titre}"' for titre in rows[0]]
    data = rows[1:]

    table_name = "BD"

    create_sql_table(database, title, table_name)
    insert_data_into_sql_table(database, title, data, table_name)

    database.close()


if __name__ == "__main__":
    update()
