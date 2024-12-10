from typing import Dict
import os

from main.core.common.database.database_repository import DatabaseRepository
from main.core.common.logger.logger import logger
from config.settings import STATIC_ROOT

class PageBdService:
    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database = database_repository

    def main(self, isbn) -> Dict[str, str]:
        try:
            infos = self.page(isbn)
        except Exception:
            return {"isbn": isbn}
        infos["dedicaces"] = self.dedicaces_album(isbn)
        infos["exlibris"] = self.exlibris_album(isbn)
        return infos


    def get_photo_dossier(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            liste_fichiers = os.listdir(path)

            name = []
            for fichier in liste_fichiers:
                if fichier.endswith(".jpeg"):
                    name.append(os.path.basename(fichier))
            return name
        else:
            return []


    def exlibris_album(self, isbn):
        image_dir = os.path.join(STATIC_ROOT, "main/images/exlibris", str(isbn))
        return self.get_photo_dossier(image_dir)


    def dedicaces_album(self, isbn):
        image_dir = os.path.join(STATIC_ROOT, "main/images/dedicaces", str(isbn))
        return self.get_photo_dossier(image_dir)

    def page(self, isbn):
        self.database.open()
        titles = ['ISBN', 'Album', 'Numero', 'Serie', 'Scenariste', 'Dessinateur', 'Couleur', 'Editeur', 'Date_de_parution',
                  'Edition', 'Nombre_de_pages', 'Cote', 'Prix_dachat', 'Annee_dachat', 'Lieu_dachat', 'Dedicace',
                  'Ex_Libris', 'Synopsis', 'Image']
        req = ("SELECT ISBN as {}, Album as {}, Numéro as {}, Série as {}, "
               "Scénariste as {}, Dessinateur as {}, Couleur as {}, "
               "Éditeur as {}, \"Date de parution\" as {}, Édition as {}, "
               "\"Nombre de page\" as {}, Cote as {}, \"Prix d'achat\" as {}, "
               "\"Année d'achat\" as {}, \"Lieu d'achat\" as {}, "
               "Dédicace as {}, \"Ex Libris\" as {}, Synopsis as {}, Image as {} "
               "FROM BD WHERE ISBN={};").format(*titles, isbn)
        logger.info(req, extra={"isbn": isbn})
        result = self.database.get_one(req)
        self.database.close()

        infos = {}
        for title in titles:
            infos[title] = result[title]
        return infos
