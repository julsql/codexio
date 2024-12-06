from typing import Dict, List
from django.db import connections

from config.settings import DATABASES
from main.core.common.database.internal.database_connexion import DatabaseConnexion


class RandomAlbumService:
    def main(self) -> Dict[str, str]:
        database_file = DATABASES['default']['NAME']
        database = DatabaseConnexion(database_file)
        database.open()

        req = "SELECT ISBN, Album, Numéro, Série, Image, Scénariste, Dessinateur, \"Date de parution\", \"Prix d'achat\", " \
              "\"Nombre de pages\", Édition, Synopsis FROM BD ORDER BY RANDOM() LIMIT 1;"
        result = database.get_one(req)
        database.close()
        print(result)
        infos = {'ISBN': result["isbn"], 'Album': result["Album"], 'Numero': result["Numéro"], 'Serie': result["Série"], 'Image': result["Image"],
                 'Scenartiste': result["Scénariste"], 'Dessinateur': result["Dessinateur"], 'Date_de_parution': result["Date de parution"],
                 'Prix_dachat': result["Prix d'achat"], 'Nombre_de_pages': result["Nombre de pages"], 'Edition': result["Édition"], 'Synopsis': result["Synopsis"]}
        return infos
