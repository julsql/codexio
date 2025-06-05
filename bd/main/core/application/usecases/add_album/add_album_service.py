from typing import Union

from babel.dates import format_date

from main.core.application.usecases.add_album.get_infos_service import GetInfosService
from main.core.domain.exceptions.album_exceptions import AlbumAlreadyExistsException, AlbumNotFoundException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.album_repository import AlbumRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.domain.ports.repositories.sheet_repository import SheetRepository


class AddAlbumService:
    def __init__(self,
                 bd_repositories: list[AlbumRepository],
                 sheet_repository: SheetRepository,
                 logging_repository: LoggerRepository) -> None:
        doc_name = "bd"
        sheet_name = "BD"
        self.isbn = None
        self.connexion = sheet_repository
        self.connexion.open(doc_name, sheet_name)
        self.get_infos_service = GetInfosService(bd_repositories, logging_repository)
        self.logging_repository = logging_repository

    def main(self, isbn: int) -> None:
        self.isbn = isbn
        self.add_album()

    def add_album(self) -> None:
        if self.connexion.double(self.isbn):
            raise AlbumAlreadyExistsException(
                f"L'album {self.isbn} existe déjà dans la base",
                self.isbn
            )

        album = self.get_infos()
        if album is None:
            raise AlbumNotFoundException(
                f"L'album {self.isbn} n'a pas été trouvé",
                self.isbn
            )
        self.add_line(album)

    def get_infos(self) -> Album:
        return self.get_infos_service.main(self.isbn)

    def add_line(self, album: Album) -> None:
        liste = self.map_to_list(album)
        self.connexion.append(liste)

    def map_to_list(self, album: Album) -> list[Union[str, int, float]]:
        """Convertit un objet Album en liste de valeurs pour le stockage"""
        mapping = {
            "ISBN": album.isbn,  # Garder comme int
            "Album": album.title,
            "Numéro": album.number,
            "Série": album.series,
            "Scénario": album.writer,
            "Dessin": album.illustrator,
            "Couleurs": album.colorist,
            "Éditeur": album.publisher,
            "Date de publication": format_date(album.publication_date, format="d MMM y",
                                               locale="fr_FR") if album.publication_date else "",
            "Édition": album.edition,
            "Pages": album.number_of_pages if album.number_of_pages else "",
            "Prix": float(album.purchase_price) if album.purchase_price else "",
            "Synopsis": album.synopsis,
            "Image": album.image
        }

        titles = ["ISBN", "Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs",
                  "Éditeur", "Date de publication", "Édition", "Pages", None, "Prix",
                  None, None, None, None, None, None, "Synopsis", "Image"]

        liste = []
        for title in titles:
            if title is None:
                liste.append("")
            elif title in mapping:
                liste.append(mapping[title])
            else:
                self.logging_repository.error(f"{title} manque")
                raise IndexError(f"{title} manque")

        return liste
