from main.core.domain.model.attachment_type import AttachmentType
from main.core.domain.model.attachments import Attachments
from main.core.domain.ports.repositories.attachments_repository import AttachmentsRepository
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class AttachmentsService:
    def __init__(self, attachments_repository: AttachmentsRepository) -> None:
        self.repository = attachments_repository

    def main_signed_copies(self, collection_id: int) -> Attachments:
        signed_copies = self.repository.get_attachments(SIGNED_COPY_FOLDER(collection_id))
        signed_copies.set_type(AttachmentType.SIGNED_COPY, collection_id)
        return signed_copies

    def main_ex_libris(self, collection_id: int) -> Attachments:
        exlibris = self.repository.get_attachments(EXLIBRIS_FOLDER(collection_id))
        exlibris.set_type(AttachmentType.EXLIBRIS, collection_id)
        return exlibris
