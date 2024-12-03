from typing import List, Dict

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.bd_repository import BdRepository


class GetInfosService:
    def __init__(self, bd_repositories: List) -> None:
        self.isbn = None
        self.repositories = bd_repositories
    
    def main(self, isbn: int) -> Dict:
        self.isbn = isbn
        for repository in self.repositories:
            try:
                infos = self.get_infos(repository)
            except Exception as _:
                pass
            else:
                return self.corriger_info(infos)
        raise AddAlbumError(f"Aucun album trouvé avec l'isbn {self.isbn}")

    def get_infos(self, repository: BdRepository) -> Dict:
        return repository.get_infos(self.isbn)

    def corriger_info(self, info: Dict) -> Dict:
        """Corriger info s'il manque des clefs"""

        keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image',
                'Prix', 'Édition', 'Pages', 'Synopsis']

        for key in keys:
            if key not in info.keys():
                info[key] = ""
        info["ISBN"] = str(self.isbn) if self.isbn > 0 else ""
        return info
