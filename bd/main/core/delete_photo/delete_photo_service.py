import os

from config.settings import STATIC_ROOT
from main.core.delete_photo.photo_repository import PhotoRepository


class DeletePhotoService:
    def __init__(self, photo_repository: PhotoRepository) -> None:
        self.dedicace_folder = os.path.join(STATIC_ROOT, 'main/images/dedicaces')
        self.exlibris_folder = os.path.join(STATIC_ROOT, 'main/images/exlibris')
        self.repository = photo_repository

    def main(self, isbn: int, photo_id: int, photo_type: str) -> bool:
        if photo_type == 'dedicaces':
            return self.repository.delete_dedicace(isbn, photo_id)
        elif photo_type == 'exlibris':
            return self.repository.delete_exlibris(isbn, photo_id)
        else:
            raise ValueError('Unknown photo type')
