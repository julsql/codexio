from abc import ABC, abstractmethod


class PageBdAttachmentsRepository(ABC):
    @abstractmethod
    def add_attachments(self, infos, isbn):
        pass
