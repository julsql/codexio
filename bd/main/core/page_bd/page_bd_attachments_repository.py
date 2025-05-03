from abc import ABC, abstractmethod


class PageBdAttachmentsRepository(ABC):
    @abstractmethod
    def get_attachments(self, infos, isbn):
        pass
