from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from main.domain.model.album import Album


@dataclass
class BD:
    isbn: int
    album: str = ""
    number: str = ""
    series: str = ""
    writer: str = ""
    illustrator: str = ""
    colorist: str = ""
    publisher: str = ""
    publication_date: Optional[date] = None
    edition: str = ""
    number_of_pages: int = 0
    rating: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    year_of_purchase: Optional[int] = None
    place_of_purchase: str = ""
    deluxe_edition: bool = False
    localisation: str = ""
    synopsis: str = ""
    image: str = ""

    @classmethod
    def from_album(cls, album: Album) -> 'BD':
        """Crée une instance de BD à partir d'un objet Album"""
        bd = cls(isbn=album.isbn)
        bd.album = album.titre
        bd.number = album.numero
        bd.series = album.serie
        bd.writer = album.scenariste
        bd.illustrator = album.dessinateur
        bd.colorist = album.coloriste
        bd.publisher = album.editeur
        bd.publication_date = album.date_publication
        bd.edition = album.edition
        bd.number_of_pages = album.nombre_pages
        bd.purchase_price = album.prix
        bd.synopsis = album.synopsis
        bd.image = album.image_url
        return bd

    def contains(self, key):
        return key in self.__dict__

    def copy(self):
        return BD(
            isbn=self.isbn,
            album=self.album,
            number=self.number,
            series=self.series,
            writer=self.writer,
            illustrator=self.illustrator,
            colorist=self.colorist,
            publisher=self.publisher,
            publication_date=self.publication_date,
            edition=self.edition,
            number_of_pages=self.number_of_pages,
            rating=self.rating,
            purchase_price=self.purchase_price,
            year_of_purchase=self.year_of_purchase,
            place_of_purchase=self.place_of_purchase,
            deluxe_edition=self.deluxe_edition,
            localisation=self.localisation,
            synopsis=self.synopsis,
            image=self.image
        )

    def to_list(self) -> list:
        """Convertit l'objet BD en dictionnaire"""
        return [
            self.isbn,
            self.album,
            self.number,
            self.series,
            self.writer,
            self.illustrator,
            self.colorist,
            self.publisher,
            self.publication_date,
            self.edition,
            self.number_of_pages,
            self.rating,
            self.purchase_price,
            self.year_of_purchase,
            self.place_of_purchase,
            self.deluxe_edition,
            self.localisation,
            "",
            "",
            self.synopsis,
            self.image
        ]
