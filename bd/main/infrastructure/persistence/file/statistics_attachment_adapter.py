from main.domain.model.statistics import Statistics
from main.domain.ports.repositories.statistics_attachment_repository import StatisticsAttachmentRepository
from main.infrastructure.persistence.file.filesystem_adapter import count_images_in_directory
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class StatisticsAttachmentAdapter(StatisticsAttachmentRepository):
    def __init__(self, dedicaces_path: str = SIGNED_COPY_FOLDER,
                 exlibris_path: str = EXLIBRIS_FOLDER):
        self.dedicaces_path = dedicaces_path
        self.exlibris_path = exlibris_path

    def get_attachment_statistics(self) -> Statistics:
        nombre_dedicaces = count_images_in_directory(self.dedicaces_path)
        nombre_exlibris = count_images_in_directory(self.exlibris_path)

        return Statistics(
            albums_count=0,
            pages_count=0,
            purchase_price_count=0,
            deluxe_edition_count=0,
            signed_copies_count=nombre_dedicaces,
            ex_libris_count=nombre_exlibris
        )
