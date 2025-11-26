from dataclasses import dataclass
from typing import Optional

from main.core.domain.model.attachment_type import AttachmentType


@dataclass
class RandomAttachment:
    isbn: int
    path: str
    type: Optional[AttachmentType]

    def __hash__(self):
        return hash((self.isbn, self.path, self.type))

    def __eq__(self, other):
        if not isinstance(other, RandomAttachment):
            return False
        return (self.isbn, self.path, self.type) == (other.isbn, other.path, other.type)

    def __str__(self):
        return f"Banner(path={self.path}, isbn={self.isbn}, type={self.type})"
