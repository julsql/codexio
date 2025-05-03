import os
from abc import ABC

from config.settings import MEDIA_ROOT
from main.core.common.folder.folder_connexion import count_images_in_directory
from main.core.statistics.statistics_attachments_repository import StatisticsAttachmentsRepository


class StatisticsAttachmentsConnexion(StatisticsAttachmentsRepository, ABC):
    SIGNED_COPY_PATH = "main/images/dedicaces"
    EX_LIBRIS_PATH = "main/images/exlibris"

    def get_information(self):
        dedicace_total = self.get_attachments_total(self.SIGNED_COPY_PATH)
        exlibris_total = self.get_attachments_total(self.EX_LIBRIS_PATH)

        infos = {}
        infos["dedicaces"] = dedicace_total
        infos["exlibris"] = exlibris_total
        return infos

    def get_attachments_total(self, path: str) -> (list[dict[str, str]], int):
        image_folder = os.path.join(MEDIA_ROOT, path)
        attachments_sum = 0
        for item in os.listdir(image_folder):
            item_path = os.path.join(image_folder, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                nb_attachment = count_images_in_directory(item_path)
                attachments_sum += nb_attachment
        return attachments_sum
