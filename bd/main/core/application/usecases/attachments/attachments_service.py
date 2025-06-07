from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.attachment_type import AttachmentType
from main.core.domain.model.attachments import Attachments
from main.core.domain.ports.repositories.attachments_repository import AttachmentsRepository
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class AttachmentsService:
    def __init__(self, attachments_repository: AttachmentsRepository) -> None:
        self.repository = attachments_repository

    def main_signed_copies(self, user: AbstractBaseUser) -> Attachments:
        collection_id = user.collections.values('id').first()['id']
        signed_copies = self.repository.get_attachments(SIGNED_COPY_FOLDER(collection_id))
        signed_copies.set_type(AttachmentType.SIGNED_COPY, collection_id)
        return signed_copies

    def main_ex_libris(self, user: AbstractBaseUser) -> Attachments:
        collection_id = user.collections.values('id').first()['id']
        exlibris = self.repository.get_attachments(EXLIBRIS_FOLDER(collection_id))
        exlibris.set_type(AttachmentType.EXLIBRIS, collection_id)
        return exlibris
