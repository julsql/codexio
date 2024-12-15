from typing import Dict

from main.core.common.database.internal.bd_model import BD


class RandomAlbumService:
    def main(self) -> Dict[str, str]:
        return BD.objects.values(
            'isbn', 'album', 'number', 'series', 'image', 'writer', 'illustrator',
            'publication_date', 'purchase_price', 'number_of_pages', 'edition', 'synopsis'
        ).order_by('?').first()
