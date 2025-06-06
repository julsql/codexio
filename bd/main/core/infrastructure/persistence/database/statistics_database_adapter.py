from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Count, Sum, IntegerField, FloatField, QuerySet
from django.db.models.functions import Cast, Coalesce, Round

from main.core.domain.model.statistics import Statistics
from main.core.domain.ports.repositories.statistics_database_repository import StatisticsDatabaseRepository
from main.core.infrastructure.persistence.database.models.bd import BD


def map_place_of_purchase(place_of_purchase_query: QuerySet) -> list[tuple[str, int]]:
    all_results = list(place_of_purchase_query)
    first_to_show = 4

    top_4 = all_results[:first_to_show]
    others = all_results[first_to_show:]

    place_of_purchase_stats = [(item['place_of_purchase'], item['count']) for item in top_4]
    other_total = sum(item['count'] for item in others)
    if other_total > 0:
        place_of_purchase_stats.append(("AUTRE", other_total))
    return place_of_purchase_stats


class StatisticsDatabaseAdapter(StatisticsDatabaseRepository):
    def get_database_statistics(self, user: AbstractBaseUser) -> Statistics:
        stats = BD.objects.filter(collection__accounts=user).aggregate(
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

        place_of_purchase_query = BD.objects.filter(collection__accounts=user).values('place_of_purchase').annotate(
            count=Count('place_of_purchase')).order_by('-count', 'place_of_purchase')

        place_of_purchase_stats = map_place_of_purchase(place_of_purchase_query)

        return Statistics(
            albums_count=stats['nombre'],
            pages_count=stats['pages'],
            purchase_price_count=stats['prix'],
            deluxe_edition_count=stats['tirage'],
            signed_copies_count=0,
            ex_libris_count=0,
            place_of_purchase_pie=place_of_purchase_stats,
        )
