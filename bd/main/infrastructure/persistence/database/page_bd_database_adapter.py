from abc import ABC
from decimal import Decimal
from typing import Optional

from main.domain.model.bd import BD as INTERNAL_MODEL_BD
from main.domain.ports.repositories.page_bd_database_repository import PageBdDatabaseRepository
from main.infrastructure.persistence.database.models import BD as DATABASE_MODEL_BD


class PageBdDatabaseAdapter(PageBdDatabaseRepository, ABC):
    def page(self, isbn: int) -> Optional[INTERNAL_MODEL_BD]:
        result = DATABASE_MODEL_BD.objects.filter(isbn=isbn).values().first()

        if result:
            return INTERNAL_MODEL_BD(
                isbn=int(result['isbn']),
                title=result['album'],
                number=result['number'],
                series=result['series'],
                writer=result['writer'],
                illustrator=result['illustrator'],
                colorist=result['colorist'],
                publisher=result['publisher'],
                publication_date=result['publication_date'],
                edition=result['edition'],
                number_of_pages=result['number_of_pages'],
                purchase_price=Decimal(str(result['purchase_price'])) if result['purchase_price'] is not None else None,
                year_of_purchase=result['year_of_purchase'],
                place_of_purchase=result['place_of_purchase'],
                synopsis=result['synopsis'],
                image=result['image'],
            )
        return None
