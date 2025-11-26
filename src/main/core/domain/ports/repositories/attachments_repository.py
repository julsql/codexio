from abc import ABC, abstractmethod

from main.core.domain.model.attachments import Attachments


class AttachmentsRepository(ABC):
    @abstractmethod
    def get_attachments(self, path: str) -> Attachments:
        pass
