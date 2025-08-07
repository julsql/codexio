import os
from typing import Union

import gspread
from google.auth import exceptions
from google.oauth2 import service_account
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound

from config.settings import GSHEET_CREDENTIALS
from main.core.domain.exceptions.sheet_exceptions import SheetConnexionException, SheetNamesException
from main.core.domain.ports.repositories.sheet_repository import SheetRepository


class SheetAdapter(SheetRepository):
    def __init__(self, doc_name, sheet_name) -> None:
        self.__OFFSET__ = 1
        self.worksheet = None
        self.doc_name = doc_name
        self.sheet_name = sheet_name
        __FILEPATH__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        credentials_path = GSHEET_CREDENTIALS
        try:
            creds = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            )
            self.client = gspread.Client(auth=creds)
        except exceptions.DefaultCredentialsError:
            self.client = None
            raise SheetConnexionException(
                "Service Google Sheets temporairement indisponible. "
                "Veuillez réessayer plus tard."
            )

    def open(self) -> None:
        if self.doc_name and self.sheet_name:
            try:
                self.worksheet = self.client.open(self.doc_name).worksheet(self.sheet_name)
            except SheetNamesException as e:
                raise SheetNamesException(f"{self.doc_name} ou {self.sheet_name} inexistant") from e
            except APIError as e:
                raise SheetConnexionException(f"{e} Erreur d'API") from e
            except SpreadsheetNotFound as e:
                raise SheetNamesException(f"Le doc {self.doc_name} n'existe pas") from e
            except WorksheetNotFound as e:
                raise SheetNamesException(f"La feuille {self.sheet_name} n'existe pas pour le doc {self.doc_name}") from e
            except Exception as e:
                raise SheetConnexionException(f"{e} Erreur inconnue") from e
        else:
            raise SheetNamesException("Il manque le nom du doc ou de la feuille")

    def append(self, liste: list[Union[str, int, float]]) -> None:
        self.worksheet.append_row(liste)

    def get(self, i: int, j: int) -> str:
        i += self.__OFFSET__
        j += self.__OFFSET__
        return self.worksheet.cell(i, j).value

    def get_line(self, i: int) -> list[str]:
        i += self.__OFFSET__
        return self.worksheet.row_values(i)

    def get_column(self, j: int) -> list[str]:
        j += self.__OFFSET__
        return self.worksheet.col_values(j)

    def get_size(self) -> (int, int):
        sheet = self.worksheet.get_all_values()
        return len(sheet), len(sheet[0])

    def get_all(self) -> list[list[str]]:
        return self.worksheet.get_all_values()

    def set(self, valeur: str, i: int, j: int) -> None:
        i += self.__OFFSET__
        j += self.__OFFSET__
        if isinstance(valeur, str):
            self.worksheet.update_cell(i, j, valeur)
        else:
            raise TypeError(f"{valeur} n'est pas un type texte")

    def set_line(self, valeur: list[str], i: int) -> None:
        i += self.__OFFSET__
        if isinstance(valeur, list):
            self.worksheet.update([valeur], f"A{i}")

    def set_column(self, valeur: list[str], j: int, offset: int) -> None:
        j += self.__OFFSET__
        offset += self.__OFFSET__
        plage_de_cellules = self.worksheet.range(offset, j, len(valeur), j)

        for i in range(len(plage_de_cellules)):
            plage_de_cellules[i].value = valeur[i]

        self.worksheet.update_cells(plage_de_cellules)

    def delete_row(self, i: int) -> None:
        self.set_line([''] * self.get_size()[1], i)

    def clear(self) -> None:
        self.worksheet.clear()

    def double(self, isbn: int) -> bool:
        row_values = self.get_column(0)

        for cell_value in row_values:
            if cell_value == str(isbn):
                return True

        return False
