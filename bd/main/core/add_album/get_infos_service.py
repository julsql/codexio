from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository
from main.core.common.logger.logger import logger


class GetInfosService:
    def __init__(self, bd_repositories: list[BdRepository]) -> None:
        self.isbn = None
        self.repositories = bd_repositories

    def main(self, isbn: int) -> dict[str, str]:
        self.isbn = isbn
        infos_complete = {}
        for repository in self.repositories:
            try:
                current_infos = self.get_infos(repository)
                # Fusion des informations
                for key, value in current_infos.items():
                    # On ne remplace que si la valeur est vide ou n'existe pas
                    if key not in infos_complete or not infos_complete[key]:
                        infos_complete[key] = value

                # Si toutes les clés requises sont remplies, on peut arrêter
                if self.is_complete(infos_complete):
                    break

            except Exception as e:
                logger.error(str(e), exc_info=True)
                logger.warning(f"{isbn} non trouvé dans {str(repository)}", exc_info=True)
                continue

        if infos_complete:
            return self.corriger_info(infos_complete)
        else:
            raise AddAlbumError(f"Aucun album trouvé avec l'isbn {self.isbn}")

    def is_complete(self, infos: dict) -> bool:
        """Vérifie si toutes les informations requises sont présentes et non vides"""
        required_keys = {
            "Album", "Série", "Numéro", "Scénario", "Dessin", "Couleurs",
            "Éditeur", "Édition", "Date de publication", "Pages", "Prix",
            "Synopsis", "Image"
        }

        return all(
            key in infos and infos[key]
            for key in required_keys
        )

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
