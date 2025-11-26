from django.db.models import Count, Sum, IntegerField, FloatField
from django.db.models.functions import Cast, Coalesce, Round

from main.core.domain.model.statistics import Statistics
from main.core.domain.ports.repositories.statistics_database_repository import StatisticsDatabaseRepository
from main.core.infrastructure.persistence.database.models.book import Book


class StatisticsBookDatabaseAdapter(StatisticsDatabaseRepository):
    def get_database_statistics(self, collection_id: int) -> Statistics:
        stats = Book.objects.filter(collection=collection_id).aggregate(
            nombre=Count('id'),
            pages=Coalesce(Sum(Cast('number_of_pages', output_field=IntegerField())), 0),
            prix=Coalesce(
                Round(
                    Sum(
                        Coalesce('purchase_price', 0.0, output_field=FloatField())
                    )
                ),
                0,
                output_field=IntegerField()
            ),
        )

        place_of_purchase_query = Book.objects.filter(collection=collection_id).values('place_of_purchase').annotate(
            count=Count('place_of_purchase')).order_by('-count', 'place_of_purchase')

        place_of_purchase_stats = self.map_place_of_purchase(place_of_purchase_query)

        return Statistics(
            albums_count=stats['nombre'],
            pages_count=stats['pages'],
            purchase_price_count=stats['prix'],
            deluxe_edition_count=0,
            signed_copies_count=0,
            ex_libris_count=0,
            place_of_purchase_pie=place_of_purchase_stats,
        )
