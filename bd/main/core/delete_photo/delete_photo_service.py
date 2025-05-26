from main.core.delete_photo.photo_repository import PhotoRepository
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class DeletePhotoService:
    def __init__(self, photo_repository: PhotoRepository) -> None:
        self.repository = photo_repository

    def main(self, isbn: int, photo_id: int, photo_type: str) -> bool:
        if photo_type == 'dedicaces':
            return self.repository.delete_photo(isbn, photo_id, SIGNED_COPY_FOLDER)
        elif photo_type == 'exlibris':
            return self.repository.delete_photo(isbn, photo_id, EXLIBRIS_FOLDER)
        else:
            raise ValueError('Unknown photo type')
