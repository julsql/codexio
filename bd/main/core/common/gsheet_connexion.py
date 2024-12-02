import gspread
from google.auth import exceptions
from google.oauth2 import service_account
import os
from main.core.add_album.add_album_error import AddAlbumError
from main.core.common.gsheet_repository import GsheetRepository


class GsheetConnexion(GsheetRepository):
    def __init__(self):
        self.__OFFSET__ = 1
        self.worksheet = None
        __FILEPATH__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        credentials_path = os.path.join(__FILEPATH__, 'private/config-sheet-91.json')
        try:
            creds = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            )
            self.client = gspread.Client(auth=creds)
        except exceptions.DefaultCredentialsError:
            message_log = "Google Sheet non accessible."
            self.client = None
            raise AddAlbumError(message_log, None)

    def open(self, doc_name: str, sheet_name: str = None):
        if sheet_name is not None:
            self.worksheet = self.client.open(doc_name).worksheet(sheet_name)
        else:
            self.worksheet = self.client.open(doc_name).sheet1

    def append(self, liste: list):
        self.worksheet.append_row(liste)

    def get(self, i: int, j: int) -> str:
        i += self.__OFFSET__
        j += self.__OFFSET__
        return self.worksheet.cell(i, j).value

    def get_line(self, i: int) -> list:
        i += self.__OFFSET__
        return self.worksheet.row_values(i)

    def get_column(self, j: int) -> list:
        j += self.__OFFSET__
        return self.worksheet.col_values(j)

    def get_all(self) -> list:
        return self.worksheet.get_all_values()

    def set(self, valeur: str, i: int, j: int):
        i += self.__OFFSET__
        j += self.__OFFSET__
        if isinstance(valeur, str):
            self.worksheet.update_cell(i, j, valeur)
        else:
            raise TypeError(f"{valeur} n'est pas un type texte")

    def set_line(self, valeur: list, i: int):
        i += self.__OFFSET__
        if isinstance(valeur, list):
            self.worksheet.update([valeur], f"A{i}")
        else:
            self.worksheet.update([[valeur]], f"A{i}")

    def set_column(self, valeur: str, j: int):
        j += self.__OFFSET__
        plage_de_cellules = self.worksheet.range(2, j, len(valeur), j)

        for i in range(len(plage_de_cellules)):
            plage_de_cellules[i].value = valeur[i]

        self.worksheet.update_cells(plage_de_cellules)

    def delete_row(self, i: int):
        self.set_line([""] * 26, i)

    def double(self, isbn: int) -> bool:
        row_values = self.get_column(0)

        for cell_value in row_values:
            if cell_value == str(isbn):
                return True

        return False
