from abc import ABC, abstractmethod

from main.core.domain.model.work_attachment import WorkAttachment


class WorkAttachmentsRepository(ABC):
    @abstractmethod
    def get_attachments(self, isbn) -> WorkAttachment:
        pass
