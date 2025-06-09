from abc import ABC, abstractmethod

from main.core.domain.model.bd_attachment import BdAttachment


class WorkAttachmentsRepository(ABC):
    @abstractmethod
    def get_attachments(self, isbn) -> BdAttachment:
        pass
