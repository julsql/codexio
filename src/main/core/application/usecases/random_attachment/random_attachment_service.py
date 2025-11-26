import os

from config.settings import STATIC_URL
from main.core.domain.model.random_attachment import RandomAttachment
from main.core.domain.ports.repositories.random_attachment_repository import RandomAttachmentRepository
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class RandomAttachmentService:

    def __init__(self, banner_repository: RandomAttachmentRepository) -> None:
        self.repository = banner_repository

    def main(self) -> RandomAttachment:
        image_files = self.repository.get_all_images_path([SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER])
        default_image_path = os.path.join(STATIC_URL, "main/images/random_attachment.jpg")
        banner = RandomAttachment(isbn=0, type=None, path=default_image_path)
        if image_files and len(image_files) > 0:
            banner = self.repository.get_random_attachment(image_files)
        return banner
