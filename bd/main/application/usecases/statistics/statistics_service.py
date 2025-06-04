from main.domain.model.statistics import Statistics
from main.domain.ports.repositories.statistics_attachment_repository import StatisticsAttachmentRepository
from main.domain.ports.repositories.statistics_database_repository import StatisticsDatabaseRepository


class StatisticsService:
    def __init__(self, database_repository: StatisticsDatabaseRepository,
                 attachment_repository: StatisticsAttachmentRepository):
        self._database_repository = database_repository
        self._attachment_repository = attachment_repository

    def execute(self) -> Statistics:
        db_stats = self._database_repository.get_database_statistics()
        attachment_stats = self._attachment_repository.get_attachment_statistics()

        return Statistics(
            albums_count=db_stats.albums_count,
            pages_count=db_stats.pages_count,
            purchase_price_count=db_stats.purchase_price_count,
            deluxe_edition_count=db_stats.deluxe_edition_count,
            signed_copies_count=attachment_stats.signed_copies_count,
            ex_libris_count=attachment_stats.ex_libris_count
        )
