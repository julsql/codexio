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
            nombre_albums=db_stats.nombre_albums,
            nombre_pages=db_stats.nombre_pages,
            prix_total=db_stats.prix_total,
            nombre_editions_speciales=db_stats.nombre_editions_speciales,
            nombre_dedicaces=attachment_stats.nombre_dedicaces,
            nombre_exlibris=attachment_stats.nombre_exlibris
        )
