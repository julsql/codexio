from main.core.statistics.statistics_attachments_repository import StatisticsAttachmentsRepository
from main.core.statistics.statistics_database_repository import StatisticsDatabaseRepository


class StatisticsService:
    SIGNED_COPY_PATH = "main/images/dedicaces"
    EX_LIBRIS_PATH = "main/images/exlibris"

    def __init__(self, attachments_repository: StatisticsAttachmentsRepository,
                 database_repository: StatisticsDatabaseRepository) -> None:
        self.attachments_repository = attachments_repository
        self.database_repository = database_repository

    def main(self) -> dict[str, int]:
        infos_database = self.database_repository.get_information()
        infos_attachments = self.attachments_repository.get_information()

        return {**infos_database, **infos_attachments}
