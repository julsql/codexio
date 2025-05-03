import os
from abc import ABC

from main.core.common.data.data import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from main.core.common.directory.directory_methods import count_images_in_directory
from main.core.statistics.statistics_attachments_repository import StatisticsAttachmentsRepository


class StatisticsAttachmentsConnexion(StatisticsAttachmentsRepository, ABC):

    def get_information(self):
        dedicace_total = self.get_attachments_total(SIGNED_COPY_FOLDER)
        exlibris_total = self.get_attachments_total(EXLIBRIS_FOLDER)

        infos = {}
        infos["dedicaces"] = dedicace_total
        infos["exlibris"] = exlibris_total
        return infos

    def get_attachments_total(self, image_folder: str) -> (list[dict[str, str]], int):
        attachments_sum = 0
        for item in os.listdir(image_folder):
            item_path = os.path.join(image_folder, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                nb_attachment = count_images_in_directory(item_path)
                attachments_sum += nb_attachment
        return attachments_sum
