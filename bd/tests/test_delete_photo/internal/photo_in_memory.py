from abc import ABC

from main.core.delete_photo.photo_repository import PhotoRepository


class PhotoInMemory(PhotoRepository, ABC):
    type = ""

    def delete_photo(self, isbn: int, photo_id: int, folder: str) -> bool:
        self.type = folder
        return True
