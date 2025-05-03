import os
import random
from abc import ABC

from config.settings import MEDIA_ROOT, MEDIA_URL
from main.core.banner.banner_repository import BannerRepository


class BannerConnexion(BannerRepository, ABC):

    def get_all_images_path(self, paths: list[str]) -> list[str]:
        return sum([self.list_files_in_subdirectories(
            os.path.join(MEDIA_ROOT, path)) for path in paths], [])

    def list_files_in_subdirectories(self, directory_path: str) -> list[str]:
        if not os.path.isdir(directory_path):
            return []

        files = []
        image_extensions = ['.jpg', '.jpeg', '.png']

        for root, dirs, files_in_root in os.walk(directory_path):
            for file_name in files_in_root:
                if any(file_name.lower().endswith(ext) for ext in image_extensions):
                    parent_directory = os.path.basename(root)
                    grandparent_directory = os.path.basename(os.path.dirname(root))
                    files.append(os.path.join(grandparent_directory, parent_directory, file_name))

        return files

    def get_random_attachment(self, images_files: list[str]) -> tuple[str, str, str]:
        random_image = random.choice(images_files)

        random_image_path = os.path.join(MEDIA_URL, "main/images/", random_image)
        random_isbn = os.path.basename(os.path.dirname(random_image_path))
        random_type = os.path.basename(os.path.dirname(os.path.dirname(random_image_path)))
        return random_image_path, random_isbn, random_type
