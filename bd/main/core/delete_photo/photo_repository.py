from abc import ABC, abstractmethod


class PhotoRepository(ABC):
    @abstractmethod
    def delete_dedicace(self, isbn: int, photo_id: int) -> int:
        pass

    @abstractmethod
    def delete_exlibris(self, isbn: int, photo_id: int) -> int:
        pass
