import os
from abc import ABC

from main.domain.model.bd_attachment import BdAttachment
from main.domain.ports.repositories.page_bd_attachments_repository import PageBdAttachmentsRepository


class PageBdAttachmentsAdapter(PageBdAttachmentsRepository, ABC):
    def __init__(self, signer_copy_folder: str, exlibris_folder: str):
        self.SIGNED_COPY_FOLDER = signer_copy_folder
        self.EXLIBRIS_FOLDER = exlibris_folder

    def get_attachments(self, isbn) -> BdAttachment:
        signed_copies = sorted(self.attachment_album(isbn, self.SIGNED_COPY_FOLDER))
        ex_libris = sorted(self.attachment_album(isbn, self.EXLIBRIS_FOLDER))
        return BdAttachment(signed_copies=signed_copies, ex_libris=ex_libris)

    def attachment_album(self, isbn: int, path: str) -> list[str]:
        image_dir = os.path.join(path, str(isbn))
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
