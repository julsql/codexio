from typing import Dict
import os

from main.core.common.database.internal.bd_model import BD
from config.settings import STATIC_ROOT

class PageBdService:

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
        fields = [
            'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist',
            'publisher', 'publication_date', 'edition', 'number_of_pages', 'rating',
            'purchase_price', 'year_of_purchase', 'place_of_purchase', 'signed_copy',
            'ex_libris', 'synopsis', 'image'
        ]
        return BD.objects.filter(isbn=isbn).values(*fields).first()
