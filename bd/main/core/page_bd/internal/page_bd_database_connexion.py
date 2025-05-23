from abc import ABC
from typing import Any

from main.infrastructure.persistence.database.models import BD
from main.core.page_bd.page_bd_database_repository import PageBdDatabaseRepository


class PageBdDatabaseConnexion(PageBdDatabaseRepository, ABC):
    def page(self, isbn: int) -> dict[str, Any] | None:
        fields = [
            'isbn', 'album', 'number', 'series', 'writer', 'illustrator', 'colorist',
            'publisher', 'publication_date', 'edition', 'number_of_pages',
            'purchase_price', 'year_of_purchase', 'place_of_purchase',
            'synopsis', 'image'
        ]
        result = BD.objects.filter(isbn=isbn).values(*fields).first()
        if result and 'purchase_price' in result and result['purchase_price'] and int(
                result['purchase_price']) == float(result['purchase_price']):
            result['purchase_price'] = int(result['purchase_price'])
        return result
