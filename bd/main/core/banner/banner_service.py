import os
import random

from config.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL


class RandomDedicaceService:
    def main(self) -> dict[str, str]:
        dedicace_folder = os.path.join(MEDIA_ROOT, 'main/images/dedicaces')
        exlibris_folder = os.path.join(MEDIA_ROOT, 'main/images/exlibris')
        image_files = self.list_files_in_subdirectories(dedicace_folder) + self.list_files_in_subdirectories(exlibris_folder)
        random_isbn = 0
        random_type = ""
        if image_files:
            random_image = random.choice(image_files)
            random_image_path = os.path.join(MEDIA_URL, "main/images/", random_image)
            random_isbn = os.path.basename(os.path.dirname(random_image_path))
            random_type = os.path.basename(os.path.dirname(os.path.dirname(random_image_path)))
        else:
            random_image_path = os.path.join(STATIC_URL, "main/images/banner.jpg")
        return {'banner_path': str(random_image_path), 'banner_isbn': random_isbn, "banner_type": random_type}

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
