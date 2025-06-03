from dataclasses import dataclass


@dataclass
class ReduceAlbum:
    isbn: int
    titre: str = ""
    numero: str = ""
    serie: str = ""
    scenariste: str = ""
    dessinateur: str = ""

    def __str__(self) -> str:
        return f"ReduceAlbum(isbn={self.isbn}, titre={self.titre}, numero={self.numero}, serie={self.serie}, " \
               f"scenariste={self.scenariste}, dessinateur={self.dessinateur})"
