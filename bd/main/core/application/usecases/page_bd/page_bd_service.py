from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.bd_with_attachment import BdWithAttachment
from main.core.domain.ports.repositories.logger_repository import LoggerRepository
from main.core.domain.ports.repositories.page_bd_attachments_repository import PageBdAttachmentsRepository
from main.core.domain.ports.repositories.page_bd_database_repository import PageBdDatabaseRepository
from main.core.infrastructure.persistence.database.models import Collection


class PageBdService:

    def __init__(self, attachments_repository: PageBdAttachmentsRepository,
                 database_repository: PageBdDatabaseRepository,
                 logger_repository: LoggerRepository) -> None:
        self.logging_repository = logger_repository
        self.attachments_repository = attachments_repository
        self.database_repository = database_repository

    def main(self, isbn: int, collection: Collection) -> Optional[BdWithAttachment]:
        try:
            album = self.database_repository.page(isbn, collection)
        except Exception as e:
            self.logging_repository.error(
                str(e),
                extra={"isbn": isbn}
            )
            return None
        if album is None:
            self.logging_repository.error(
                "ISBN manquant dans la base",
                extra={"isbn": isbn}
            )
            return None
        attachments = self.attachments_repository.get_attachments(isbn)
        return BdWithAttachment(album=album, attachments=attachments)
