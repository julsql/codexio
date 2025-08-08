from typing import Union

from babel.dates import format_date

from main.core.application.usecases.add_album.get_infos_service import GetInfosService
from main.core.domain.exceptions.album_exceptions import AlbumAlreadyExistsException, AlbumNotFoundException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.add_album_repository import AddAlbumRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.domain.ports.repositories.sheet_repository import SheetRepository


class AddBookService:
    def __init__(self,
                 book_repositories: list[AddAlbumRepository],
                 sheet_repository: SheetRepository,
                 logging_repository: LoggerRepository) -> None:
        self.isbn = None
        self.connexion = sheet_repository
        self.connexion.open()
        self.get_infos_service = GetInfosService(book_repositories, logging_repository)
        self.logging_repository = logging_repository

    def main(self, isbn: int) -> None:
        self.isbn = isbn
        self.add_book()

    def add_book(self) -> None:
        if self.connexion.double(self.isbn):
            raise AlbumAlreadyExistsException(
                f"Le livre {self.isbn} existe déjà dans la base",
                self.isbn
            )

        album = self.get_infos()
        if album is None:
            raise AlbumNotFoundException(
                f"Le livre {self.isbn} n'a pas été trouvé",
                self.isbn
            )
        self.add_line(album)

    def get_infos(self) -> Album:
        return self.get_infos_service.main(self.isbn)

    def add_line(self, album: Album) -> None:
        liste = self.map_to_list(album)
        self.connexion.append(liste)

    def map_to_list(self, book: Album) -> list[Union[str, int, float]]:
        """Convertit un objet Book en liste de valeurs pour le stockage"""
        mapping = {
            "ISBN": book.isbn,
            "Titre": book.title,
            "Auteur": book.writer,
            "Traducteur": book.translator,
            "Éditeur": book.publisher,
            "Collection": book.collection_book,
            "Date de parution": format_date(book.publication_date, format="d MMM y",
                                            locale="fr_FR") if book.publication_date else "",
            "Édition": book.edition,
            "Nombre de pages": book.number_of_pages if book.number_of_pages else "",
            "Genre littéraire": book.literary_genre,
            "Style": book.style,
            "Langue d'origine": book.origin_language,
            "Synopsis": book.synopsis,
            "Image": book.image
        }

        titles = ["ISBN", "Titre", "Auteur", "Traducteur", "Éditeur", "Collection", "Date de parution",
                  "Édition", "Nombre de pages", "Genre littéraire", "Style", "Langue d'origine", None,
                  None, None, None, "Synopsis", "Image"]

        liste = []
        for title in titles:
            if title is None:
                liste.append("")
            elif title in mapping:
                liste.append(mapping[title])
            else:
                self.logging_repository.error(f"{title} manque")
                print(f"{title} manque")
                raise IndexError(f"{title} manque")

        return liste