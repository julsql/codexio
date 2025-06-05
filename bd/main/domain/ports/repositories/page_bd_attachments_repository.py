from abc import ABC, abstractmethod

from main.domain.model.bd_attachment import BdAttachment


class PageBdAttachmentsRepository(ABC):
    @abstractmethod
    def get_attachments(self, isbn) -> BdAttachment:
        pass
