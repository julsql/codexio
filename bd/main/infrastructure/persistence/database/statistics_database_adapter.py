from django.db.models import Count, Sum, IntegerField, FloatField
from django.db.models.functions import Cast, Coalesce, Round

from main.domain.model.statistics import Statistics
from main.domain.ports.repositories.statistics_database_repository import StatisticsDatabaseRepository
from main.infrastructure.persistence.database.models import BD


class StatisticsDatabaseAdapter(StatisticsDatabaseRepository):
    def get_database_statistics(self) -> Statistics:
        stats = BD.objects.aggregate(
            nombre=Count('id'),
            pages=Coalesce(Sum(Cast('number_of_pages', output_field=IntegerField())), 0),
            prix=Coalesce(
                Round(
                    Sum(
                        Coalesce('rating', 0.0, output_field=FloatField())
                    )
                ),
                0,
                output_field=IntegerField()
            ),
            tirage=Coalesce(Sum(Cast('deluxe_edition', output_field=IntegerField())), 0),
        )

        return Statistics(
            nombre_albums=stats['nombre'],
            nombre_pages=stats['pages'],
            prix_total=stats['prix'],
            nombre_editions_speciales=stats['tirage'],
            nombre_dedicaces=0,
            nombre_exlibris=0
        )
