from main.core.add_album.bd_repository import BdRepository


class GetInfosService:
    def __init__(self, isbn: int, bd_repositories: list):
        self.isbn = isbn
        self.repositories = bd_repositories
    
    def main(self):
        for repository in self.repositories:
            try:
                infos = self.get_infos(repository)
            except Exception as _:
                return None
            else:
                return self.corriger_info(infos)
        raise ValueError(f"Aucun album trouvé avec l'isbn {self.isbn}")

    def get_infos(self, repository: BdRepository):
        return repository.get_infos(self.isbn)

    def corriger_info(self, info):
        """Corriger info s'il manque des clefs"""

        keys = ['Série', 'Numéro', 'Album', 'Scénario', 'Dessin', 'Couleurs', 'Éditeur', 'Date de publication', 'Image',
                'Prix', 'Édition', 'Pages', 'Synopsis']

        for key in keys:
            if key not in info.keys():
                info[key] = ""
        info["ISBN"] = self.isbn
        return info