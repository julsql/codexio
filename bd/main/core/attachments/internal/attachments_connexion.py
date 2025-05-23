import os
from abc import ABC

from main.core.attachments.attachments_repository import AttachmentsRepository
from main.infrastructure.persistence.database.models import BD
from main.core.common.directory.directory_methods import count_images_in_directory


class AttachmentsConnexion(AttachmentsRepository, ABC):

    def get_attachments(self, path: str) -> (list[dict[str, str]], int):
        image_folder = path
        infos = []
        attachments_sum = 0
        for item in os.listdir(image_folder):
            item_path = os.path.join(image_folder, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                isbn = item
                nb_attachments = count_images_in_directory(item_path)
                result = BD.objects.filter(isbn=isbn).values('album', 'number', 'series').first()
                attachments_sum += nb_attachments
                if result is None:
                    infos.append({'isbn': isbn, 'album': "", 'number': "", 'series': "",
                                  'range': range(1, nb_attachments + 1), 'attachments': nb_attachments})
                else:
                    infos.append(
                        {'isbn': isbn, 'album': result["album"], 'number': result["number"], 'series': result["series"],
                         'range': range(1, nb_attachments + 1), 'attachments': nb_attachments})
        return infos, attachments_sum
