from datetime import date
from decimal import Decimal
from typing import Optional

from main.core.domain.model.bd import BD
from main.core.domain.ports.repositories.sheet_repository import SheetRepository
from main.core.domain.ports.repositories.table_bd_repository import DatabaseRepository
from main.core.infrastructure.api.internal.date_parser_service import DateParserService
from main.core.infrastructure.persistence.database.models import Collection


class UpdateDatabaseService:
    def __init__(self, sheet_repository: SheetRepository, database_repository: DatabaseRepository) -> None:
        self.sheet = sheet_repository
        self.sheet.open()
        self.database = database_repository

    def main(self, collection: Collection) -> None:
        rows = self.sheet.get_all()
        titles = self.map_sheet_titles_to_database_columns(rows[0])

        data = self._process_rows(rows[1:], rows[0], titles)

        self.database.reset_table(collection)
        self.database.insert(data, collection)

    def _process_rows(self, rows: list[list[str]], column_titles: list[str], titles: list[str]) -> list[BD]:
        data = []
        for row_index in range(len(rows)):
            row = rows[row_index]
            isbn = self.convert_isbn(self._get_isbn(row, titles))
            if isbn is not None:
                processed_row = BD(isbn=isbn)
                for column_index in range(len(row)):
                    title = titles[column_index]
                    if title not in ("signed_copy", "ex_libris"):
                        try:
                            self._convert_cell_value(processed_row, row[column_index], title, isbn)
                        except Exception:
                            raise ValueError(
                                f"Erreur lors de la conversion de la colonne `{column_titles[column_index]}` ligne {row_index + 2}")
                data.append(processed_row)
        return data

    def _get_isbn(self, row: list[str], titles: list[str]) -> str:
        return row[titles.index("isbn")]

    def _convert_cell_value(self, bd: BD, value: str, title: str, isbn: int) -> any:
        match title:
            case "isbn":
                bd.isbn = isbn
            case "album":
                bd.title = value
            case "number":
                bd.number = value
            case "series":
                bd.series = value
            case "writer":
                bd.writer = value
            case "illustrator":
                bd.illustrator = value
            case "colorist":
                bd.colorist = value
            case "publisher":
                bd.publisher = value
            case "publication_date":
                bd.publication_date = self.convert_date(value)
            case "edition":
                bd.edition = value
            case "number_of_pages":
                bd.number_of_pages = self.convert_int(value)
            case "rating":
                bd.rating = self.convert_price(value)
            case "purchase_price":
                bd.purchase_price = self.convert_price(value)
            case "year_of_purchase":
                bd.year_of_purchase = self.convert_int(value)
            case "place_of_purchase":
                bd.place_of_purchase = value
            case "deluxe_edition":
                bd.deluxe_edition = value.lower() == "oui"
            case "signed_copy":
                bd.signed_copy = value
            case "ex_libris":
                bd.ex_libris = value
            case "localisation":
                bd.localisation = value
            case "synopsis":
                bd.synopsis = value
            case "image":
                bd.image = value

    def convert_isbn(self, isbn: str) -> int | None:
        if isbn:
            try:
                return int(isbn.replace("-", ""))
            except ValueError:
                return None
        else:
            return None

    def convert_int(self, year: str) -> Optional[int]:
        if year:
            return int(year)
        else:
            return None

    def convert_date(self, date_str: str) -> Optional[date]:
        return DateParserService.parse_date(date_str)

    def convert_price(self, price: str) -> Optional[Decimal]:
        if price:
            return Decimal(price.replace(",", "."))
        else:
            return None

    def map_sheet_titles_to_database_columns(self, sheet_titles: list[str]) -> list[str]:
        mapper = {"isbn": "isbn",
                  "album": "album",
                  "numéro": "number",
                  "série": "series",
                  "scénariste": "writer",
                  "dessinateur": "illustrator",
                  "couleur": "colorist",
                  "éditeur": "publisher",
                  "date de parution": "publication_date",
                  "édition": "edition",
                  "nombre de planches": "number_of_pages",
                  "cote": "rating",
                  "prix d'achat": "purchase_price",
                  "année d'achat": "year_of_purchase",
                  "lieu d'achat": "place_of_purchase",
                  "tirage de tête": "deluxe_edition",
                  "dédicace": "signed_copy",
                  "ex libris": "ex_libris",
                  "emplacement": "localisation",
                  "synopsis": "synopsis",
                  "image": "image"
                  }

        return [mapper[titre.lower()] for titre in sheet_titles]
