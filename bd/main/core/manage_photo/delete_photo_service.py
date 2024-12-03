import os

from config.settings import STATIC_ROOT


class DeletePhotoService:
    ALLOWED_EXTENSIONS = '.jpeg'
    DEDICACE_FOLDER = os.path.join(STATIC_ROOT, 'main/images/dedicaces')
    EXLIBRIS_FOLDER = os.path.join(STATIC_ROOT, 'main/images/exlibris')

    def main(self, isbn: int, photo_id: int, photo_type: str) -> int:
        if photo_type == 'dedicaces':
            origin_folder = self.DEDICACE_FOLDER
        else:
            origin_folder = self.EXLIBRIS_FOLDER

        album_path = os.path.join(origin_folder, str(isbn))
        image_path = os.path.join(album_path, f"{photo_id}{self.ALLOWED_EXTENSIONS}")
        image_exists = os.path.exists(image_path)
        if image_exists:
            os.remove(image_path)
            if not any(os.listdir(album_path)):
                os.rmdir(album_path)
            else:
                self.renommer_photos(album_path)
        return image_exists

    def renommer_photos(self, chemin_dossier):
        fichiers = os.listdir(chemin_dossier)

        fichiers_photos = [f for f in fichiers if f.endswith(self.ALLOWED_EXTENSIONS)]
        fichiers_photos.sort(key=lambda x: int(x.split('.')[0]))

        for i, fichier in enumerate(fichiers_photos, start=1):
            ancien_chemin = os.path.join(chemin_dossier, fichier)
            nouveau_nom = f"{i}{self.ALLOWED_EXTENSIONS}"
            nouveau_chemin = os.path.join(chemin_dossier, nouveau_nom)

            os.rename(ancien_chemin, nouveau_chemin)