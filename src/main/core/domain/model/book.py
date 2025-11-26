from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from main.core.domain.model.album import Album


@dataclass
class Book:
    isbn: int
    title: str = ""
    writer: str = ""
    translator: str = ""
    publisher: str = ""
    collection_book: str = ""
    publication_date: Optional[date] = None
    edition: str = ""
    number_of_pages: int = 0
    literary_genre: str = ""
    style: str = ""
    origin_language: str = ""
    purchase_price: Optional[Decimal] = None
    year_of_purchase: Optional[int] = None
    place_of_purchase: str = ""
    localisation: str = ""
    synopsis: str = ""
    image: str = ""

    @classmethod
    def from_album(cls, album: Album) -> 'Book':
        """Crée une instance de Book à partir d'un objet Album"""
        book = cls(isbn=album.isbn)
        book.title = album.title
        book.writer = album.writer
        book.publication_date = album.publication_date
        book.edition = album.edition
        book.number_of_pages = album.number_of_pages
        book.purchase_price = album.purchase_price
        book.synopsis = album.synopsis
        book.image = album.image
        return book

    def contains(self, key: str) -> bool:
        return key in self.__dict__

    def copy(self) -> 'Book':
        return Book(
            isbn=self.isbn,
            title=self.title,
            writer=self.writer,
            translator=self.translator,
            publisher=self.publisher,
            collection_book=self.collection_book,
            publication_date=self.publication_date,
            edition=self.edition,
            number_of_pages=self.number_of_pages,
            literary_genre=self.literary_genre,
            style=self.style,
            origin_language=self.origin_language,
            purchase_price=self.purchase_price,
            year_of_purchase=self.year_of_purchase,
            place_of_purchase=self.place_of_purchase,
            localisation=self.localisation,
            synopsis=self.synopsis,
            image=self.image
        )

    def to_list(self) -> list:
        """Convertit l'objet Book en liste (équivalent d'une ligne de feuille Excel par exemple)"""
        return [
            self.isbn,
            self.title,
            self.writer,
            self.translator,
            self.publisher,
            self.collection_book,
            self.publication_date,
            self.edition,
            self.number_of_pages,
            self.literary_genre,
            self.style,
            self.origin_language,
            self.purchase_price,
            self.year_of_purchase,
            self.place_of_purchase,
            self.localisation,
            "", "",  # champs libres
            self.synopsis,
            self.image
        ]

    def __str__(self) -> str:
        return (
            f"Book(isbn={self.isbn}, title={self.title}, writer={self.writer}, translator={self.translator}, "
            f"publisher={self.publisher}, collection_book={self.collection_book}, publication_date={self.publication_date}, "
            f"edition={self.edition}, number_of_pages={self.number_of_pages}, literary_genre={self.literary_genre}, "
            f"style={self.style}, origin_language={self.origin_language}, purchase_price={self.purchase_price}, "
            f"year_of_purchase={self.year_of_purchase}, place_of_purchase={self.place_of_purchase}, "
            f"localisation={self.localisation}, synopsis={self.synopsis}, image={self.image})"
        )
