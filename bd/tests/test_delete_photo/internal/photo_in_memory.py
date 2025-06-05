from abc import ABC

from main.core.domain import DeletePhotoRepository


class DeletePhotoInMemory(DeletePhotoRepository, ABC):
    type = ""

    def delete_photo(self, isbn: int, photo_id: int, folder: str) -> bool:
        self.type = folder
        return True
