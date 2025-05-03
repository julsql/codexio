from typing import Any

from main.core.page_bd.page_bd_attachments_repository import PageBdAttachmentsRepository
from main.core.page_bd.page_bd_database_repository import PageBdDatabaseRepository


class PageBdAttachmentsInMemory(PageBdAttachmentsRepository):
    def __init__(self):
        self.added_attachments = []
        self.last_isbn = None
        self.last_infos = None

    def get_attachments(self, infos, isbn):
        self.last_isbn = isbn
        self.last_infos = infos
        self.added_attachments.append((infos, isbn))


class PageBdDatabaseInMemory(PageBdDatabaseRepository):
    def __init__(self):
        self.data = {}
        self.should_raise_error = False

    def add_bd(self, isbn: int, info: dict):
        self.data[isbn] = info

    def set_error(self, should_raise: bool):
        self.should_raise_error = should_raise

    def page(self, isbn: int) -> dict[str, Any] | None:
        if self.should_raise_error:
            raise Exception("Test database error")
        if isbn not in self.data:
            raise Exception("ISBN missing")
        return self.data.get(isbn)
