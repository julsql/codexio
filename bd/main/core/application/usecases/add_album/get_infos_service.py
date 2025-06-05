from decimal import Decimal

from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.album_repository import AlbumRepository
from main.core.domain.ports.repositories.logger_repository import LoggerRepository


class GetInfosService:
    def __init__(self,
                 bd_repositories: list[AlbumRepository],
                 logging_repository: LoggerRepository) -> None:
        self.isbn = None
        self.repositories = bd_repositories
        self.logging_repository = logging_repository

    def main(self, isbn: int) -> Album:
        self.isbn = isbn
        album_complet = Album(isbn=isbn)

        if not self.repositories:
            raise AlbumNotFoundException(f"Aucun repository disponible pour l'ISBN {isbn}", isbn)

        for repository in self.repositories:
            try:
                current_album = repository.get_infos(self.isbn)
                # Fusion des informations
                album_complet = self.fusionner_albums(album_complet, current_album)

                # Si toutes les informations requises sont remplies, on peut arrêter
                if album_complet.is_complete():
                    break

            except Exception as e:
                self.logging_repository.error(
                    f"Erreur lors de la récupération des informations depuis {str(repository)}: {str(e)}"
                )

        if album_complet.is_empty():
            raise AlbumNotFoundException(f"Album {isbn} non trouvé", isbn)

        return album_complet

    def fusionner_albums(self, album_base: Album, album_nouveau: Album) -> Album:
        """Fusionne deux albums en ne remplaçant que les valeurs vides"""
        if not album_nouveau:
            return album_base

        # Pour chaque attribut de l'album
        for attr in vars(album_base):
            valeur_base = getattr(album_base, attr)
            valeur_nouvelle = getattr(album_nouveau, attr, None)

            # On ne remplace que si la valeur de base est vide et la nouvelle non vide
            if self.est_valeur_vide(valeur_base) and not self.est_valeur_vide(valeur_nouvelle):
                setattr(album_base, attr, valeur_nouvelle)

        return album_base

    @staticmethod
    def est_valeur_vide(valeur) -> bool:
        """Vérifie si une valeur est considérée comme vide"""
        if valeur is None:
            return True
        if isinstance(valeur, str) and valeur == "":
            return True
        if isinstance(valeur, (int, Decimal)) and valeur == 0:
            return True
        return False
