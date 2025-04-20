from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger


class GetInfosService:
    def __init__(self, bd_repositories: list[BdRepository]) -> None:
        self.isbn = None
        self.repositories = bd_repositories

    def main(self, isbn: int) -> dict[str, str]:
        self.isbn = isbn
        for repository in self.repositories:
            try:
                infos = self.get_infos(repository)
            except Exception as e:
                logger.error(str(e), exc_info=True)
                logger.warning(f"{isbn} non trouvé dans {str(repository)}", exc_info=True)
            else:
                return self.corriger_info(infos)
        raise AddAlbumError(f"Aucun album trouvé avec l'isbn {self.isbn}")

    def get_infos(self, repository: BdRepository) -> dict[str, str | float | int]:
        return repository.get_infos(self.isbn)

    def corriger_info(self, info: dict[str, str]) -> dict[str, str]:
        """Corriger info s'il manque des clefs"""

        keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image',
                'Prix', 'Édition', 'Pages', 'Synopsis']

        for key in keys:
            if key not in info.keys():
                info[key] = ""
        info["ISBN"] = str(self.isbn) if self.isbn > 0 else ""
        return info
