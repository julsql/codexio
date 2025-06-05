import os
from abc import ABC

from main.domain.ports.repositories.delete_photo_repository import DeletePhotoRepository


class DeleteDeletePhotoAdapter(DeletePhotoRepository, ABC):

    def __init__(self):
        self.allowed_extensions = '.jpeg'

    def delete_photo(self, isbn: int, photo_id: int, folder: str) -> bool:
        album_path = os.path.join(folder, str(isbn))
        image_path = os.path.join(album_path, f"{photo_id}{self.allowed_extensions}")
        image_exists = os.path.exists(image_path)
        if image_exists:
            os.remove(image_path)
            if not any(os.listdir(album_path)):
                os.rmdir(album_path)
            else:
                self.renommer_photos(album_path)
        return image_exists

    def renommer_photos(self, chemin_dossier) -> None:
        fichiers = os.listdir(chemin_dossier)

        fichiers_photos = [f for f in fichiers if f.endswith(self.allowed_extensions)]
        fichiers_photos.sort(key=lambda x: int(x.split('.')[0]))

        for i, fichier in enumerate(fichiers_photos, start=1):
            ancien_chemin = os.path.join(chemin_dossier, fichier)
            nouveau_nom = f"{i}{self.allowed_extensions}"
            nouveau_chemin = os.path.join(chemin_dossier, nouveau_nom)

            os.rename(ancien_chemin, nouveau_chemin)
