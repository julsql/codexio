from main.core.common.database.database_repository import DatabaseRepository
from main.core.common.sheet.sheet_repository import SheetRepository

class UpdateDatabaseService:
    def __init__(self, sheet_repository: SheetRepository, database_repository: DatabaseRepository) -> None:
        doc_name = "bd"
        sheet_name = "BD"
        self.sheet = sheet_repository
        self.sheet.open(doc_name, sheet_name)
        self.database = database_repository

    def main(self) -> None:
        rows = self.sheet.get_all()
        title = self.map_sheet_titles_to_database_columns(rows[0])

        data = [{title[i] : row[i] for i in range(len(row))} for row in rows[1:]]

        self.database.create_table()
        self.database.insert(data)

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
                  "synopsis": "synopsis",
                  "image": "image"
                  }

        return [mapper[titre.lower()] for titre in sheet_titles]
