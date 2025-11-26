from abc import ABC
from decimal import Decimal
from typing import Optional

from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.random_album_repository import RandomAlbumRepository
from main.core.infrastructure.persistence.database.models.book import Book as Book_database


class RandomBookAdapter(RandomAlbumRepository, ABC):

    def get_random_album(self, collection_id: int) -> Optional[Album]:
        result = Book_database.objects.filter(collection=collection_id).values(
            'isbn', 'title', 'writer', 'translator', 'publisher', 'collection_book', 'publication_date',
            'edition', 'number_of_pages', 'literary_genre', 'style', 'origin_language', 'purchase_price', 'synopsis', 'image'
        ).order_by('?').first()

        random_album = Album(0)

        if result:
            random_album = Album(
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
                synopsis=result['synopsis'],
                image=result['image'],
            )
        return random_album
