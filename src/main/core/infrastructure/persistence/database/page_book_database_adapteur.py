from abc import ABC
from decimal import Decimal
from typing import Optional

from main.core.domain.model.book import Book as INTERNAL_MODEL_BOOK
from main.core.domain.ports.repositories.page_bd_database_repository import WorkDatabaseRepository
from main.core.infrastructure.persistence.database.models.book import Book as DATABASE_MODEL_BOOK


class WorkDatabaseBookAdapter(WorkDatabaseRepository, ABC):
    def page(self, isbn: int, collection_id: int) -> Optional[INTERNAL_MODEL_BOOK]:
        result = DATABASE_MODEL_BOOK.objects.filter(collection=collection_id).filter(isbn=isbn).values().first()

        if result:
            return INTERNAL_MODEL_BOOK(
                isbn=int(result['isbn']),
                title=result['title'],
                writer=result['writer'],
                translator=result['translator'],
                publisher=result['publisher'],
                collection_book=result['collection_book'],
                publication_date=result['publication_date'],
                edition=result['edition'],
                number_of_pages=result['number_of_pages'],
                literary_genre=result['literary_genre'],
                style=result['style'],
                origin_language=result['origin_language'],
                purchase_price=Decimal(str(result['purchase_price'])) if result['purchase_price'] is not None else None,
                year_of_purchase=result['year_of_purchase'],
                place_of_purchase=result['place_of_purchase'],
                localisation=result['localisation'],
                synopsis=result['synopsis'],
                image=result['image'],
            )
        return None
