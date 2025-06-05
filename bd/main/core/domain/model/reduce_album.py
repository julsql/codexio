from dataclasses import dataclass


@dataclass
class ReduceAlbum:
    isbn: int
    title: str = ""
    number: str = ""
    series: str = ""
    writer: str = ""
    illustrator: str = ""

    def __str__(self) -> str:
        return f"ReduceAlbum(isbn={self.isbn}, title={self.title}, number={self.number}, series={self.series}, " \
               f"writer={self.writer}, illustrator={self.illustrator})"
