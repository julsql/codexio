from abc import ABC

from main.core.delete_photo.photo_repository import PhotoRepository


class PhotoInMemory(PhotoRepository, ABC):
    type = ""

    def delete_dedicace(self, isbn: int, photo_id: int) -> bool:
        self.type = "dedicaces"
        return True

    def delete_exlibris(self, isbn: int, photo_id: int) -> bool:
        self.type = "exlibris"
        return True
