from abc import ABC, abstractmethod


class PageBdAttachmentsRepository(ABC):
    @abstractmethod
    def add_attachments(self, infos, isbn):
        pass

    @abstractmethod
    def attachment_album(self, isbn: int, path: str) -> list[str]:
        pass

    @abstractmethod
    def get_photo_dossier(self, path: str) -> list[str]:
        pass
