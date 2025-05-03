import os
from abc import ABC

from main.core.common.directory.directory_methods import count_images_in_directory
from main.core.statistics.statistics_attachments_repository import StatisticsAttachmentsRepository


class StatisticsAttachmentsConnexion(StatisticsAttachmentsRepository, ABC):

    def __init__(self, signer_copy_folder: str, exlibris_folder: str):
        self.SIGNED_COPY_FOLDER = signer_copy_folder
        self.EXLIBRIS_FOLDER = exlibris_folder

    def get_information(self):
        dedicace_total = self.get_attachments_total(self.SIGNED_COPY_FOLDER)
        exlibris_total = self.get_attachments_total(self.EXLIBRIS_FOLDER)

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
