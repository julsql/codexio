import gspread
from google.auth import exceptions
from google.oauth2 import service_account
import os
from error import Error


class Conn:

    def __init__(self):
        self.__OFFSET__ = 1
        self.worksheet = None
        __FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(__FILEPATH__, 'private/bd-sheet-91-c65d6c5a0f0b.json')
        try:
            creds = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            )
            self.client = gspread.Client(auth=creds)
            self.client.login()
        except exceptions.DefaultCredentialsError:
            message_log = "Google Sheet non accessible."
            Error(message_log)
            self.client = None
            raise

    def open(self, doc_name, sheet_name=None):
        if sheet_name is not None:
            self.worksheet = self.client.open(doc_name).worksheet(sheet_name)
        else:
            self.worksheet = self.client.open(doc_name).sheet1

    def append(self, liste):
        self.worksheet.append_row(liste)

    def get(self, i, j):
        i += self.__OFFSET__
        j += self.__OFFSET__
        return self.worksheet.cell(i, j + self.__OFFSET__).value

    def get_line(self, i):
        i += self.__OFFSET__
        return self.worksheet.row_values(i)

    def get_column(self, j):
        j += self.__OFFSET__
        return self.worksheet.col_values(j)

    def get_all(self):
        return self.worksheet.get_all_values()

    def set(self, valeur, i, j):
        i += self.__OFFSET__
        j += self.__OFFSET__
        if type(valeur) is type(""):
            self.worksheet.update_cell(i, j, valeur)
        else:
            raise TypeError(f"{valeur} is not str type")

    def set_line(self, valeur, i):
        i += self.__OFFSET__
        if type(valeur) is type(list()):
            self.worksheet.update(f"A{i}", [valeur])
        else:
            self.worksheet.update(f"A{i}", [[valeur]])

    def double(self, isbn):
        # Récupérer les valeurs de la ligne spécifiée (row_index)
        row_values = self.get_column(0)

        # Parcourir les cellules de la ligne et vérifier si l'une d'entre elles a la valeur cible
        for cell_value in row_values:
            if cell_value == isbn:
                return True

        return False  # La valeur cible n'a pas été trouvée dans la ligne
