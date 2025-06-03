from abc import ABC
from decimal import Decimal
from typing import Optional

from main.domain.model.album import Album
from main.domain.ports.repositories.random_album_repository import RandomAlbumRepository
from main.infrastructure.persistence.database.models import BD


class RandomAlbumAdapter(RandomAlbumRepository, ABC):

    def get_random_album(self) -> Optional[Album]:
        result = BD.objects.values(
            'isbn', 'album', 'number', 'series', 'image', 'writer', 'illustrator',
            'publication_date', 'purchase_price', 'number_of_pages', 'edition', 'synopsis'
        ).order_by('?').first()

        random_album = Album(0)

        if result:
            random_album = Album(
                isbn=int(result['isbn']),
                titre=result['album'],
                numero=result['number'],
                serie=result['series'],
                image_url=result['image'],
                scenariste=result['writer'],
                dessinateur=result['illustrator'],
                date_publication=result['publication_date'],
                purchase_price=Decimal(str(result['purchase_price'])) if result['purchase_price'] is not None else None,
                nombre_pages=result['number_of_pages'],
                edition=result['edition'],
                synopsis=result['synopsis'],
            )
        return random_album
