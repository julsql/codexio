from dataclasses import dataclass

from main.core.domain.model.book import Book
from main.core.domain.model.work_attachment import WorkAttachment


@dataclass
class BookWithAttachment:
    album: Book
    attachments: WorkAttachment

    def __str__(self) -> str:
        return f"BookWithAttachment(album={self.album}, attachments={self.attachments})"
