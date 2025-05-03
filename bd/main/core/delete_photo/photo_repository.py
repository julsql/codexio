from abc import ABC, abstractmethod


class PhotoRepository(ABC):

    @abstractmethod
    def delete_photo(self, isbn: int, photo_id: int, folder: str) -> bool:
        pass
