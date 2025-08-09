from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser

from main.core.domain.model.bd import BD
from main.core.domain.model.work_attachment import WorkAttachment
from main.core.domain.ports.repositories.page_bd_attachments_repository import WorkAttachmentsRepository
from main.core.domain.ports.repositories.page_bd_database_repository import WorkDatabaseRepository


class WorkAttachmentsInMemory(WorkAttachmentsRepository):
    def __init__(self):
        self.added_attachments = []
        self.last_isbn = None

    def get_attachments(self, isbn) -> WorkAttachment:
        self.last_isbn = isbn
        self.added_attachments.append(isbn)
        return WorkAttachment(signed_copies=[], ex_libris=[])


class WorkDatabaseInMemory(WorkDatabaseRepository):
    def __init__(self):
        self.data = {}
        self.should_raise_error = False

    def add_bd(self, isbn: int, info: BD):
        self.data[isbn] = info

    def set_error(self, should_raise: bool):
        self.should_raise_error = should_raise

    def page(self, isbn: int, user: AbstractBaseUser) -> Optional[BD]:
        if self.should_raise_error:
            raise Exception("Test database error")
        if isbn not in self.data:
            raise Exception("ISBN missing")
        return self.data.get(isbn)
