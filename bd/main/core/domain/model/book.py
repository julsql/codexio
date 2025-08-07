from dataclasses import dataclass
from datetime import date
from typing import Optional


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
    synopsis: str = ""
    image: str = ""

    def is_complete(self) -> bool:
        return all([
            self.title != "",
            self.writer != "",
            self.translator != "",
            self.publisher != "",
            self.collection_book != "",
            self.publication_date is not None,
            self.edition != "",
            self.number_of_pages > 0,
            self.literary_genre != "",
            self.style != "",
            self.origin_language != "",
            self.synopsis != "",
            self.image != ""
        ])

    def is_empty(self) -> bool:
        return all([
            self.title == "",
            self.writer == "",
            self.translator == "",
            self.publisher == "",
            self.collection_book == "",
            self.publication_date is None,
            self.edition == "",
            self.number_of_pages == 0,
            self.literary_genre == "",
            self.style == "",
            self.origin_language == "",
            self.synopsis == "",
            self.image == ""
        ])

def __str__(self):
    return f"Book(isbn={self.isbn}, title={self.title}, writer={self.writer}, translator={self.translator}, " \
           f"publisher={self.publisher}, collection_book={self.collection_book}, " \
           f"publication_date={self.publication_date}, edition={self.edition}, " \
           f"number_of_pages={self.number_of_pages}, literary_genre={self.literary_genre}, " \
           f"style={self.style}, synopsis={self.synopsis}, image={self.image})"
