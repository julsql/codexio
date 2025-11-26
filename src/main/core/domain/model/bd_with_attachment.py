from dataclasses import dataclass

from main.core.domain.model.bd import BD
from main.core.domain.model.work_attachment import WorkAttachment


@dataclass
class BdWithAttachment:
    album: BD
    attachments: WorkAttachment

    def __str__(self) -> str:
        return f"BdWithAttachment(album={self.album}, attachments={self.attachments})"
