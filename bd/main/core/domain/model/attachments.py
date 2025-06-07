from dataclasses import dataclass, field

from main.core.domain.model.attachment import Attachment
from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH


@dataclass
class Attachments:
    attachments_list: list[Attachment]
    sum: int = field(init=False)
    title: str = ""
    subtitle: str = ""
    type: str = ""
    image_path: str = ""

    def __post_init__(self):
        self.sum = sum([attachment.total for attachment in self.attachments_list])

    def set_type(self, attachment_type: AttachmentType, collection_id: int):
        if attachment_type == AttachmentType.SIGNED_COPY:
            self.title = 'dédicaces'
            self.subtitle = 'Toutes les dédicaces'
            self.type = 'dédicace'
            self.image_path = SIGNED_COPY_PATH(collection_id)
        if attachment_type == AttachmentType.EXLIBRIS:
            self.title = 'Ex-libris'
            self.subtitle = 'Tous les ex-libris'
            self.type = 'ex-libris'
            self.image_path = EXLIBRIS_PATH(collection_id)

    def __str__(self):
        return (
            f"Attachments(attachments_list={', '.join(str(attachment) for attachment in self.attachments_list)}, "
            f"sum={self.sum}, title={self.title}, subtitle={self.subtitle}, image_path={self.image_path})"
        )
