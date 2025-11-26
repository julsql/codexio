from main.core.domain.model.attachments import Attachments
from main.core.domain.ports.repositories.attachments_repository import AttachmentsRepository


class AttachmentsInMemory(AttachmentsRepository):
    def __init__(self) -> None:
        self.attachments = {}

    def get_attachments(self, path: str) -> Attachments:
        if path not in self.attachments:
            return Attachments(attachments_list=[])

        attachments = self.attachments[path]
        return Attachments(attachments_list=attachments)
