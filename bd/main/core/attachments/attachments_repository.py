from abc import ABC, abstractmethod


class AttachmentsRepository(ABC):
    @abstractmethod
    def get_attachments(self, path: str) -> (list[dict[str, str]], int):
        pass
