from typing import Any
import os

from main.core.common.database.internal.bd_model import BD
from config.settings import MEDIA_ROOT
from main.core.common.logger.logger import logger


class PageBdService:

    def main(self, isbn: int) -> dict[str, str]:
        try:
            infos = self.page(isbn)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return {"isbn": str(isbn)}
        infos["dedicaces"] = sorted(self.dedicaces_album(isbn))
        infos["nb_dedicace"] = len(infos["dedicaces"])
        infos["ex_libris"] = sorted(self.exlibris_album(isbn))
        infos["nb_exlibris"] = len(infos["ex_libris"])
        return infos


    def get_photo_dossier(self, path: str) -> list[str]:
        if os.path.exists(path) and os.path.isdir(path):
            liste_fichiers = os.listdir(path)

            name = []
            for fichier in liste_fichiers:
                if fichier.endswith(".jpeg"):
                    name.append(os.path.basename(fichier))
            return name
        else:
            return []


    def exlibris_album(self, isbn: int) -> list[str]:
        image_dir = os.path.join(MEDIA_ROOT, "main/images/exlibris", str(isbn))
        return self.get_photo_dossier(image_dir)


    def dedicaces_album(self, isbn: int) -> list[str]:
        image_dir = os.path.join(MEDIA_ROOT, "main/images/dedicaces", str(isbn))
        return self.get_photo_dossier(image_dir)

    def page(self, isbn: int) -> dict[str, Any] | None:
        fields = [
            'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist',
            'publisher', 'publication_date', 'edition', 'number_of_pages', 'rating',
            'purchase_price', 'year_of_purchase', 'place_of_purchase',
            'synopsis', 'image'
        ]
        return BD.objects.filter(isbn=isbn).values(*fields).first()
