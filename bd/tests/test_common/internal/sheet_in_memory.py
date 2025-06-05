from typing import Union

from main.core.domain.ports.repositories.sheet_repository import SheetRepository


class SheetInMemory(SheetRepository):

    def __init__(self) -> None:
        self.worksheet = []
        self.client = {"bd": {"BD": [], "Test": []}}
        self.__OFFSET__ = 0

    def open(self, doc_name: str, sheet_name: str = None) -> None:
        return None

    def append(self, liste: list[Union[str, int, float]]) -> None:
        self.worksheet.append(liste)

    def get(self, i: int, j: int) -> str:
        i += self.__OFFSET__
        j += self.__OFFSET__
        return self.worksheet[i][j]

    def get_line(self, i: int) -> list[str]:
        i += self.__OFFSET__
        return [self.get(i, j) for j in range(len(self.worksheet[i]))]

    def get_column(self, j: int) -> list[str]:
        j += self.__OFFSET__

        return [row[j] for row in self.worksheet]

    def get_size(self) -> (int, int):
        return len(self.worksheet), len(self.worksheet[0])

    def get_all(self) -> list[list[str]]:
        return self.worksheet

    def set(self, valeur: str, i: int, j: int) -> None:
        i += self.__OFFSET__
        j += self.__OFFSET__
        if isinstance(valeur, str):
            self.worksheet[i][j] = valeur
        else:
            raise TypeError(f"{valeur} n'est pas un type texte")

    def set_line(self, valeur: list[str], i: int) -> None:
        i += self.__OFFSET__
        if i < len(self.worksheet):
            if isinstance(valeur, list):
                self.worksheet[i] = valeur
            else:
                self.worksheet[i] = [valeur]

    def set_column(self, valeur: list[str], j: int, offset: int) -> None:
        for i in range(len(self.worksheet)):
            if len(self.worksheet[i]) < j:
                self.worksheet[i][j] = valeur[i]

    def delete_row(self, i: int) -> None:
        self.set_line([''] * self.get_size()[1], i)

    def clear(self) -> None:
        self.worksheet = []

    def double(self, isbn: int) -> bool:
        row_values = self.get_column(0)
        for cell_value in row_values:
            if str(cell_value) == str(isbn):
                return True
        return False
