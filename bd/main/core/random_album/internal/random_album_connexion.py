from abc import ABC
from typing import Any

from main.infrastructure.persistence.database.models import BD
from main.core.random_album.random_album_repository import RandomAlbumRepository


class RandomAlbumConnexion(RandomAlbumRepository, ABC):

    def get_random_album(self) -> dict[str, Any] | None:
        result = BD.objects.values(
            'isbn', 'album', 'number', 'series', 'image', 'writer', 'illustrator',
            'publication_date', 'purchase_price', 'number_of_pages', 'edition', 'synopsis'
        ).order_by('?').first()

        if result and int(result['purchase_price']) == float(result['purchase_price']):
            result['purchase_price'] = int(result['purchase_price'])
        return result
