from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.get_infos_service import GetInfosService
from main.core.common.sheet_repository import SheetRepository
from main.core.common.logger import logger


class AddAlbumService:
    def __init__(self, isbn: int, bd_repositories: list, sheet_repository: SheetRepository):
        doc_name = "bd"
        sheet_name = "BD"
        self.isbn = isbn
        self.connexion = sheet_repository
        self.connexion.open(doc_name, sheet_name)
        self.get_infos_service = GetInfosService(self.isbn, bd_repositories)

    def main(self):
        return self.add_album()

    def add_album(self):
        if self.connexion.double(self.isbn):
            message_log = f"{self.isbn} est déjà dans la base de données"
            raise AddAlbumError(message_log, self.isbn)

        infos = self.get_infos()
        self.add_line(infos)
        return infos

    def get_infos(self) -> dict:
        return self.get_infos_service.main()

    def add_line(self, infos):
        liste = self.map_to_list(infos)
        self.connexion.append(liste)

    def map_to_list(self, infos: dict) -> list:
        titles = ["ISBN", "Album", "Numéro", "Série", "Scénario", "Dessin", "Couleurs",
                  "Éditeur", "Date de publication", "Édition", "Pages", None, "Prix", None, None, None, None, None, "Synopsis",
                  "Image"]

        liste = []
        for title in titles:
            if title in infos:
                liste.append(infos[title])
            elif title is None:
                liste.append("")
            else:
                logger.error(f"{title} manque")
                raise IndexError(f"{title} manque")
        return liste
