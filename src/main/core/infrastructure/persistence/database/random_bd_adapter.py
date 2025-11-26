from abc import ABC
from decimal import Decimal
from typing import Optional

from main.core.domain.model.album import Album
from main.core.domain.ports.repositories.random_album_repository import RandomAlbumRepository
from main.core.infrastructure.persistence.database.models.bd import BD


class RandomBdAdapter(RandomAlbumRepository, ABC):

    def get_random_album(self, collection_id: int) -> Optional[Album]:
        result = BD.objects.filter(collection=collection_id).values(
            'isbn', 'album', 'number', 'series', 'image', 'writer', 'illustrator',
            'publication_date', 'purchase_price', 'number_of_pages', 'edition', 'synopsis'
        ).order_by('?').first()

        random_album = Album(0)

        if result:
            random_album = Album(
                isbn=int(result['isbn']),
                title=result['album'],
                number=result['number'],
                series=result['series'],
                image=result['image'],
                writer=result['writer'],
                illustrator=result['illustrator'],
                publication_date=result['publication_date'],
                purchase_price=Decimal(str(result['purchase_price'])) if result['purchase_price'] is not None else None,
                number_of_pages=result['number_of_pages'],
                edition=result['edition'],
                synopsis=result['synopsis'],
            )
        return random_album
