from datetime import datetime

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
        titles = self.map_sheet_titles_to_database_columns(rows[0])

        isbn_index = titles.index("isbn")
        deluxe_edition_index = titles.index("deluxe_edition")
        publication_date_index = titles.index("publication_date")
        purchase_price_index = titles.index("purchase_price")
        number_of_pages_index = titles.index("number_of_pages")
        rating_index = titles.index("rating")
        year_of_purchase_index = titles.index("year_of_purchase")
        signed_copy_index = titles.index("signed_copy")
        ex_libris_index = titles.index("ex_libris")

        data = []

        for row in rows[1:]:
            isbn = self.convert_isbn(row[isbn_index])
            if isbn is not None:
                data.append({titles[i]:
                                 (row[i].lower() == "oui" if i == deluxe_edition_index else
                                  isbn if i == isbn_index else
                                  self.convert_date(row[i]) if i == publication_date_index else
                                  self.convert_price(row[i]) if i == purchase_price_index else
                                  self.convert_int(row[i]) if i == number_of_pages_index else
                                  self.convert_price(row[i]) if i == rating_index else
                                  self.convert_int(row[i]) if i == year_of_purchase_index else
                                  row[i])
                             for i in range(len(row))
                             if i != signed_copy_index and i != ex_libris_index})

        titles.remove("signed_copy")
        titles.remove("ex_libris")

        self.database.create_table()
        self.database.insert(data)

    def convert_isbn(self, isbn: str) -> int|None:
        if isbn:
            try:
                return int(isbn.replace("-", ""))
            except ValueError:
                return None
        else:
            return None

    def convert_date(self, date: str) -> str|None:
        # Dictionnaire des mois français
        mois_fr = {
            "janv.": "01", "févr.": "02", "mars": "03", "avr.": "04", "mai": "05", "juin": "06",
            "juil.": "07", "août": "08", "sept.": "09", "oct.": "10", "nov.": "11", "déc.": "12",
            "janvier": "01", "février": "02", "avril": "04",
            "juillet": "07", "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
        }

        date_str = date.strip()  # Supprimer les espaces inutiles

        # Format déjà correct : YYYY-MM-DD
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass

        # Format YYYY-MM → Ajoute le 1er jour du mois
        try:
            return datetime.strptime(date_str, "%Y-%m").strftime("%Y-%m-01")
        except ValueError:
            pass

        # Format YYYY-M-D → Complète avec des zéros si nécessaire
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass

        # Format "17 juin 2022" (jour mois année en français)
        try:
            jour, mois_francais, annee = date_str.split()
            mois = mois_fr[mois_francais.lower()]  # Convertir le mois
            return f"{annee}-{mois}-{int(jour):02d}"
        except (ValueError, KeyError):
            pass

        return None

    def convert_int(self, year: str) -> int|None :
        if year:
            return int(year)
        else:
            return None

    def convert_price(self, price: str) -> float|None :
        if price:
            return float(price.replace(",", "."))
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