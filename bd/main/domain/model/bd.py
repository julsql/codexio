from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from main.domain.model.album import Album


@dataclass
class BD:
    isbn: int
    title: str = ""
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
        bd.title = album.title
        bd.number = album.number
        bd.series = album.series
        bd.writer = album.writer
        bd.illustrator = album.illustrator
        bd.colorist = album.colorist
        bd.publisher = album.publisher
        bd.publication_date = album.publication_date
        bd.edition = album.edition
        bd.number_of_pages = album.number_of_pages
        bd.purchase_price = album.purchase_price
        bd.synopsis = album.synopsis
        bd.image = album.image
        return bd

    def contains(self, key):
        return key in self.__dict__

    def copy(self):
        return BD(
            isbn=self.isbn,
            title=self.title,
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
            self.title,
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

    def __str__(self):
        return f"BD(isbn={self.isbn}, title={self.title}, number={self.number}, series={self.series}, " \
               f"writer={self.writer}, illustrator={self.illustrator}, colorist={self.colorist}, " \
               f"publisher={self.publisher}, publication_date={self.publication_date}, edition={self.edition}, " \
               f"number_of_pages={self.number_of_pages}, rating={self.rating}, purchase_price={self.purchase_price}, " \
               f"year_of_purchase={self.year_of_purchase}, place_of_purchase={self.place_of_purchase}, " \
               f"deluxe_edition={self.deluxe_edition}, localisation={self.localisation}, synopsis={self.synopsis}, " \
               f"image={self.image})"