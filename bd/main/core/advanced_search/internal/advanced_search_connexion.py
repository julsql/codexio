from abc import ABC
from typing import Any

from django.db.models import QuerySet

from main.core.advanced_search.advanced_search_repository import AdvancedSearchRepository
from main.core.common.database.internal.bd_model import BD


class AdvancedSearchConnexion(AdvancedSearchRepository, ABC):

    def get_all(self) -> QuerySet[BD, BD]:
        return BD.objects.all()

    def get_by_form(self, data: dict[str, Any], queryset: QuerySet[BD, BD]) -> QuerySet[BD, BD]:
        filters = {
            'isbn__icontains': 'isbn',
            'album__icontains': 'album',
            'number__icontains': 'number',
            'series__icontains': 'series',
            'writer__icontains': 'writer',
            'illustrator__icontains': 'illustrator',
            'publisher__icontains': 'publisher',
            'edition__icontains': 'edition',
            'year_of_purchase': 'year_of_purchase',
            'deluxe_edition': 'deluxe_edition',
        }

        # Appliquer les filtres
        queryset = queryset.filter(**{
            field_name: data[form_field_name]
            for field_name, form_field_name in filters.items()
            if data.get(form_field_name)
        })

        # Filtrer par synopsis
        if synopsis := data.get('synopsis'):
            queryset = queryset.filter(synopsis__icontains=" ".join(synopsis.split()))

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(publication_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(publication_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(publication_date__lte=end_date)
        return queryset

    def order_by(self, queryset: QuerySet[BD], criteria: bool, croissant: bool) -> QuerySet[BD]:
        return queryset.order_by(criteria if croissant else f"-{criteria}")
