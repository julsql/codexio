from typing import Dict

from main.core.common.database.internal.bd_model import BD


class RandomAlbumService:
    def main(self) -> Dict[str, str]:

        result  = BD.objects.values(
            'isbn', 'album', 'number', 'series', 'image', 'writer', 'illustrator',
            'publication_date', 'purchase_price', 'number_of_pages', 'edition', 'synopsis'
        ).order_by('?').first()
        infos = {'ISBN': result["isbn"], 'Album': result["album"], 'Numero': result["number"], 'Serie': result["series"], 'Image': result["image"],
                 'Scenartiste': result["writer"], 'Dessinateur': result["illustrator"], 'Date_de_parution': result["publication_date"],
                 'Prix_dachat': result["purchase_price"], 'Nombre_de_pages': result["number_of_pages"], 'Edition': result["edition"], 'Synopsis': result["synopsis"]}
        return infos
