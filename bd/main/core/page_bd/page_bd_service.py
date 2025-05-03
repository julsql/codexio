from main.core.common.logger.logger import logger
from main.core.page_bd.page_bd_attachments_repository import PageBdAttachmentsRepository
from main.core.page_bd.page_bd_database_repository import PageBdDatabaseRepository


class PageBdService:

    def __init__(self, attachments_repository: PageBdAttachmentsRepository,
                 database_repository: PageBdDatabaseRepository) -> None:
        self.attachments_repository = attachments_repository
        self.database_repository = database_repository

    def main(self, isbn: int) -> dict[str, str]:
        try:
            infos = self.database_repository.page(isbn)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return {"isbn": str(isbn)}
        self.attachments_repository.get_attachments(infos, isbn)
        return infos
