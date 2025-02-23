from typing import Any

from main.core.common.database.internal.bd_model import BD


class RandomAlbumConnexion:

    def get_random_album(self) -> dict[str, Any] | None:
        result = BD.objects.values(
            'isbn', 'album', 'number', 'series', 'image', 'writer', 'illustrator',
            'publication_date', 'purchase_price', 'number_of_pages', 'edition', 'synopsis'
        ).order_by('?').first()

        if int(result['purchase_price']) == float(result['purchase_price']):
            result['purchase_price'] = int(result['purchase_price'])
        return result
