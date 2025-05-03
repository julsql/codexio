import os
from abc import ABC

from config.settings import MEDIA_ROOT
from main.core.page_bd.page_bd_attachments_repository import PageBdAttachmentsRepository


class PageBdAttachmentsConnexion(PageBdAttachmentsRepository, ABC):
    SIGNED_COPY_PATH = "main/images/dedicaces"
    EX_LIBRIS_PATH = "main/images/exlibris"

    def add_attachments(self, infos, isbn):
        infos["dedicaces"] = sorted(self.attachment_album(isbn, self.SIGNED_COPY_PATH))
        infos["nb_dedicace"] = len(infos["dedicaces"])
        infos["ex_libris"] = sorted(self.attachment_album(isbn, self.EX_LIBRIS_PATH))
        infos["nb_exlibris"] = len(infos["ex_libris"])

    def attachment_album(self, isbn: int, path: str) -> list[str]:
        image_dir = os.path.join(MEDIA_ROOT, path, str(isbn))
        return self.get_photo_dossier(image_dir)

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
