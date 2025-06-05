from dataclasses import dataclass

from main.domain.model.bd import BD
from main.domain.model.bd_attachment import BdAttachment


@dataclass
class BdWithAttachment:
    album: BD
    attachments: BdAttachment

    def __str__(self) -> str:
        return f"BdWithAttachment(album={self.album}, attachments={self.attachments})"
