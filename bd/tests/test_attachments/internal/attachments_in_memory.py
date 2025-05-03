from main.core.attachments.attachments_repository import AttachmentsRepository


class AttachmentsInMemory(AttachmentsRepository):
    def __init__(self) -> None:
        self.attachments = {}

    def get_attachments(self, path: str) -> (list[dict[str, str]], int):
        if path not in self.attachments:
            return [], 0

        attachments = self.attachments[path]
        return attachments, len(attachments)
