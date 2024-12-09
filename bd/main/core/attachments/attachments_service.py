from typing import Dict
import os
from main.core.common.database.database_repository import DatabaseRepository
from django.conf import settings

class AttachmentsService:
    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database = database_repository

    def main(self) -> Dict[str, str]:
        dedicaces, dedicaces_sum = self.dedicaces()
        exlibris, exlibris_sum = self.exlibris()
        return {'dedicaces': dedicaces, 'dedicaces_sum': dedicaces_sum,
                'exlibris': exlibris, 'exlibris_sum': exlibris_sum}

    def dedicaces(self):
        image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/dedicaces")
        self.database.open()
        infos = []
        dedicaces_sum = 0
        for item in os.listdir(image_dir):
            item_path = os.path.join(image_dir, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                isbn = item
                nb_dedicace = self.count_images_in_directory(item_path)
                req = f"SELECT Album, Numéro, Série FROM BD WHERE ISBN = {isbn};"
                result = self.database.get_one(req)
                dedicaces_sum += nb_dedicace
                if result is None:
                    infos.append({'ISBN': isbn, 'Album': "", 'Numero': "", 'Serie': "",
                                  'DedicaceRange': range(1, nb_dedicace + 1), 'Dedicace': nb_dedicace})
                else:

                    infos.append({'ISBN': isbn, 'Album': result["Album"], 'Numero': result["Numéro"], 'Serie': result["Série"],
                                  'DedicaceRange': range(1, nb_dedicace + 1), 'Dedicace': nb_dedicace})
        self.database.close()
        return infos, dedicaces_sum


    def exlibris(self):
        image_dir = os.path.join(settings.BASE_DIR, "main/static/main/images/exlibris")
        infos = []
        self.database.open()
        exlibris_sum = 0
        for item in os.listdir(image_dir):
            item_path = os.path.join(image_dir, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                isbn = item
                nb_exlibris = self.count_images_in_directory(item_path)
                req = f"SELECT Album, Numéro, Série FROM BD WHERE ISBN = {isbn};"
                result = self.database.get_one(req)
                exlibris_sum += nb_exlibris
                if result is None:
                    infos.append({'ISBN': isbn, 'Album': "", 'Numero': "", 'Serie': "",
                                  'ExlibrisRange': range(1, nb_exlibris + 1), 'Exlibris': nb_exlibris})
                else:
                    infos.append({'ISBN': isbn, 'Album': result["Album"], 'Numero': result["Numéro"], 'Serie': result["Série"],
                                  'ExlibrisRange': range(1, nb_exlibris + 1), 'Exlibris': nb_exlibris})
        self.database.close()
        return infos, exlibris_sum


    def count_images_in_directory(self, directory_path):
        if not os.path.isdir(directory_path):
            return 0

        image_count = 0
        allowed_image_extensions = ".jpeg"

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension == allowed_image_extensions:
                    image_count += 1

        return image_count
