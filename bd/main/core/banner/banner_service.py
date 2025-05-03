import os

from config.settings import STATIC_URL
from main.core.banner.banner_repository import BannerRepository
from main.core.common.data.data import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class BannerService:

    def __init__(self, banner_repository: BannerRepository) -> None:
        self.repository = banner_repository

    def main(self) -> dict[str, str]:
        image_files = self.repository.get_all_images_path([SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER])
        random_isbn = 0
        random_type = ""
        if image_files and len(image_files) > 0:
            random_image_path, random_isbn, random_type = self.repository.get_random_attachment(
                image_files)
        else:
            random_image_path = os.path.join(STATIC_URL, "main/images/banner.jpg")
        return {'banner_path': str(random_image_path), 'banner_isbn': random_isbn, "banner_type": random_type}
