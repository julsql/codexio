from abc import ABC

from django.db.models import Count, Sum, IntegerField, FloatField
from django.db.models.functions import Cast, Round, Coalesce

from main.core.common.database.internal.bd_model import BD
from main.core.statistics.statistics_database_repository import StatisticsDatabaseRepository


class StatisticsDatabaseConnexion(StatisticsDatabaseRepository, ABC):
    def get_information(self):
        return BD.objects.aggregate(
            nombre=Count('id'),
            pages=Coalesce(Sum(Cast('number_of_pages', output_field=IntegerField())), 0),
            prix=Cast(Round(Sum(Cast('rating', output_field=FloatField()))), output_field=IntegerField()),
            tirage=Coalesce(Sum(Cast('deluxe_edition', output_field=IntegerField())), 0),
        )
