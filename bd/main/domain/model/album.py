from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Album:
    isbn: int
    titre: str = ""
    numero: str = ""
    serie: str = ""
    scenariste: str = ""
    dessinateur: str = ""
    coloriste: str = ""
    editeur: str = ""
    date_publication: Optional[date] = None
    edition: str = ""
    nombre_pages: int = 0
    prix: Optional[Decimal] = None
    synopsis: str = ""
    image_url: str = ""

    def is_complete(self) -> bool:
        return all([
            self.titre != "",
            self.numero != "",
            self.serie != "",
            self.scenariste != "",
            self.dessinateur != "",
            self.coloriste != "",
            self.editeur != "",
            self.date_publication is not None,
            self.edition != "",
            self.nombre_pages > 0,
            self.prix is not None,
            self.synopsis != "",
            self.image_url != ""
        ])

    def is_empty(self) -> bool:
        return all([
            self.titre == "",
            self.numero == "",
            self.serie == "",
            self.scenariste == "",
            self.dessinateur == "",
            self.coloriste == "",
            self.editeur == "",
            self.date_publication is None,
            self.edition == "",
            self.nombre_pages == 0,
            self.prix is None,
            self.synopsis == "",
            self.image_url == ""
        ])

    def copy(self):
        return Album(
            isbn=self.isbn,
            titre=self.titre,
            numero=self.numero,
            serie=self.serie,
            scenariste=self.scenariste,
            dessinateur=self.dessinateur,
            coloriste=self.coloriste,
            editeur=self.editeur,
            date_publication=self.date_publication,
            edition=self.edition,
            nombre_pages=self.nombre_pages,
            prix=self.prix,
            synopsis=self.synopsis,
            image_url=self.image_url,
        )

    def contains(self, key):
        return key in self.__dict__

    def __str__(self) -> str:
        return f"Album(isbn={self.isbn}, titre={self.titre}, numero={self.numero}, serie={self.serie}, " \
               f"scenariste={self.scenariste}, dessinateur={self.dessinateur}, coloriste={self.coloriste}, " \
               f"editeur={self.editeur}, date_publication={self.date_publication}, edition={self.edition}, " \
               f"nombre_pages={self.nombre_pages}, prix={self.prix}, synopsis={self.synopsis}, " \
               f"image_url={self.image_url})"
