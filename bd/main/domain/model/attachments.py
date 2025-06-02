from dataclasses import dataclass, field
from typing import Literal

from main.domain.model.attachment import Attachment
from main.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH


@dataclass
class Attachments:
    attachments_list: list[Attachment]
    sum: int = field(init=False)
    title: str = ""
    subtitle: str = ""
    image_path: str = ""

    def __post_init__(self):
        self.sum = sum([attachment.total for attachment in self.attachments_list])

    def set_type(self, attachment_type: Literal["SIGNED_COPY", "EXLIBRIS"]):
        if attachment_type == "SIGNED_COPY":
            self.title = 'dédicaces'
            self.subtitle = 'dédicaces'
            self.image_path = SIGNED_COPY_PATH
        if attachment_type == "EXLIBRIS":
            self.title = 'Ex-libris'
            self.subtitle = 'ex-libris'
            self.image_path = EXLIBRIS_PATH

    def __str__(self):
        return (
            f"Attachments(attachments={', '.join(str(attachment) for attachment in self.attachments_list)}, "
            f"sum={self.sum}, title={self.title}, subtitle={self.subtitle}, image_path={self.image_path})"
        )
