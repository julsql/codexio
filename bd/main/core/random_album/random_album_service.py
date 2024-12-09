from typing import Dict

from main.core.common.database.database_repository import DatabaseRepository


class RandomAlbumService:
    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database = database_repository

    def main(self) -> Dict[str, str]:
        self.database.open()

        req = "SELECT ISBN, Album, Numéro, Série, Image, Scénariste, Dessinateur, \"Date de parution\", \"Prix d'achat\", " \
              "\"Nombre de pages\", Édition, Synopsis FROM BD ORDER BY RANDOM() LIMIT 1;"
        result = self.database.get_one(req)
        self.database.close()
        print(result)
        infos = {'ISBN': result["isbn"], 'Album': result["Album"], 'Numero': result["Numéro"], 'Serie': result["Série"], 'Image': result["Image"],
                 'Scenartiste': result["Scénariste"], 'Dessinateur': result["Dessinateur"], 'Date_de_parution': result["Date de parution"],
                 'Prix_dachat': result["Prix d'achat"], 'Nombre_de_pages': result["Nombre de pages"], 'Edition': result["Édition"], 'Synopsis': result["Synopsis"]}
        return infos
