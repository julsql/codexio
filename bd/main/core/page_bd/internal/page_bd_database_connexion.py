from abc import ABC
from typing import Any

from main.core.common.database.internal.bd_model import BD
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
        if int(result['purchase_price']) == float(result['purchase_price']):
            result['purchase_price'] = int(result['purchase_price'])
        return result
