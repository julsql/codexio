from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Album:
    isbn: int
    title: str = ""
    number: str = ""
    series: str = ""
    writer: str = ""
    illustrator: str = ""
    translator: str = ""
    colorist: str = ""
    publisher: str = ""
    collection_book: str = ""
    literary_genre: str = ""
    style: str = ""
    origin_language: str = ""
    publication_date: Optional[date] = None
    edition: str = ""
    number_of_pages: int = 0
    purchase_price: Optional[Decimal] = None
    synopsis: str = ""
    image: str = ""

    def is_complete(self) -> bool:
        return all([
            self.title != "",
            self.number != "",
            self.series != "",
            self.writer != "",
            self.illustrator != "",
            self.colorist != "",
            self.publisher != "",
            self.publication_date is not None,
            self.edition != "",
            self.number_of_pages != 0,
            self.purchase_price is not None,
            self.synopsis != "",
            self.image != ""
        ]) or all([
            self.title != "",
            self.series != "",
            self.writer != "",
            self.translator != "",
            self.publisher != "",
            self.collection_book != "",
            self.literary_genre != "",
            self.style != "",
            self.origin_language != "",
            self.publication_date is not None,
            self.edition != "",
            self.number_of_pages > 0,
            self.purchase_price is not None,
            self.synopsis != "",
            self.image != ""
        ])

    def is_empty(self) -> bool:
        return all([
            self.title == "",
            self.number == "",
            self.series == "",
            self.writer == "",
            self.illustrator == "",
            self.colorist == "",
            self.publisher == "",
            self.publication_date is None,
            self.edition == "",
            self.number_of_pages == 0,
            self.purchase_price is None,
            self.synopsis == "",
            self.image == ""
        ]) or all([
            self.title == "",
            self.series == "",
            self.writer == "",
            self.translator == "",
            self.publisher == "",
            self.collection_book == "",
            self.literary_genre == "",
            self.style == "",
            self.origin_language == "",
            self.publication_date is None,
            self.edition == "",
            self.number_of_pages == 0,
            self.purchase_price is None,
            self.synopsis == "",
            self.image == ""
        ])

    def copy(self):
        return Album(
            isbn=self.isbn,
            title=self.title,
            number=self.number,
            series=self.series,
            writer=self.writer,
            illustrator=self.illustrator,
            translator=self.translator,
            colorist=self.colorist,
            publisher=self.publisher,
            collection_book=self.collection_book,
            literary_genre=self.literary_genre,
            style=self.style,
            origin_language=self.origin_language,
            publication_date=self.publication_date,
            edition=self.edition,
            number_of_pages=self.number_of_pages,
            purchase_price=self.purchase_price,
            synopsis=self.synopsis,
            image=self.image,
        )

    def contains(self, key):
        return key in self.__dict__

    def __str__(self) -> str:
        return f"Album(isbn={self.isbn}, title={self.title}, number={self.number}, series={self.series}, " \
               f"writer={self.writer}, illustrator={self.illustrator}, translator={self.translator}, colorist={self.colorist}, " \
               f"collection_book={self.collection_book}, literary_genre={self.literary_genre}, style={self.style}, origin_language={self.origin_language}, " \
               f"publisher={self.publisher}, publication_date={self.publication_date}, edition={self.edition}, " \
               f"number_of_pages={self.number_of_pages}, purchase_price={self.purchase_price}, synopsis={self.synopsis}, " \
               f"image={self.image})"
