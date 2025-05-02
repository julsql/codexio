import os

from django.db.models import Count, Sum, IntegerField, FloatField
from django.db.models.functions import Cast, Round, Coalesce

from config.settings import MEDIA_ROOT
from main.core.common.database.internal.bd_model import BD


class StatisticsService:
    def main(self) -> dict[str, int]:
        dedicace_total = self.get_dedicaces_total()
        exlibris_total = self.get_exlibris_total()
        infos = BD.objects.aggregate(
            nombre=Count('id'),
            pages=Coalesce(Sum(Cast('number_of_pages', output_field=IntegerField())), 0),
            prix=Cast(Round(Sum(Cast('rating', output_field=FloatField()))), output_field=IntegerField()),
            tirage=Coalesce(Sum(Cast('deluxe_edition', output_field=IntegerField())), 0),
        )
        infos["dedicaces"] = dedicace_total
        infos["exlibris"] = exlibris_total
        return infos

    def get_dedicaces_total(self) -> (list[dict[str, str]], int):
        image_folder = os.path.join(MEDIA_ROOT, 'main/images/dedicaces')
        dedicaces_sum = 0
        for item in os.listdir(image_folder):
            item_path = os.path.join(image_folder, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                nb_dedicace = self.count_images_in_directory(item_path)
                dedicaces_sum += nb_dedicace
        return dedicaces_sum

    def get_exlibris_total(self) -> (list[dict[str, str]], int):
        image_folder = os.path.join(MEDIA_ROOT, 'main/images/exlibris')
        exlibris_sum = 0
        for item in os.listdir(image_folder):
            item_path = os.path.join(image_folder, item)

            # Vérifiez si l'élément est un répertoire
            if os.path.isdir(item_path):
                nb_exlibris = self.count_images_in_directory(item_path)
                exlibris_sum += nb_exlibris
        return exlibris_sum

    def count_images_in_directory(self, directory_path: str) -> int:
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
