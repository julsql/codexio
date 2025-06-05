from main.core.domain.model.attachment_type import AttachmentType
from main.core.domain.model.attachments import Attachments
from main.core.domain.ports.repositories.attachments_repository import AttachmentsRepository
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class AttachmentsService:
    def __init__(self, attachments_repository: AttachmentsRepository) -> None:
        self.repository = attachments_repository

    def main_signed_copies(self) -> Attachments:
        signed_copies = self.repository.get_attachments(SIGNED_COPY_FOLDER)
        signed_copies.set_type(AttachmentType.SIGNED_COPY)
        return signed_copies

    def main_ex_libris(self) -> Attachments:
        exlibris = self.repository.get_attachments(EXLIBRIS_FOLDER)
        exlibris.set_type(AttachmentType.EXLIBRIS)
        return exlibris
