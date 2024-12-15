from typing import Dict

from django.db.models import Count, Sum, IntegerField, Case, When
from django.db.models.functions import Cast
from main.core.common.database.internal.bd_model import BD

class StatisticsService:
    def main(self) -> Dict[str, int]:
        return BD.objects.aggregate(
            nombre=Count('id'),
            pages=Cast(Sum('number_of_pages'), output_field=IntegerField()),
            dedicaces=Cast(Sum('signed_copy'), output_field=IntegerField()),
            exlibris=Cast(Sum('ex_libris'), output_field=IntegerField()),
            prix=Cast(Sum('rating'), output_field=IntegerField()),
            tirage=Count(
                Case(
                    When(deluxe_edition__iexact='oui', then=1)  # Compte uniquement les "Tirage de tête" = 'oui'
                )
            )
        )
