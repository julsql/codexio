from main.core.domain.model.statistics import Statistics
from main.core.domain.ports.repositories.statistics_attachment_repository import StatisticsAttachmentRepository
from main.core.infrastructure.persistence.file.filesystem_adapter import count_images_in_directory
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class StatisticsAttachmentAdapter(StatisticsAttachmentRepository):
    def __init__(self, signed_copy_path: str = SIGNED_COPY_FOLDER,
                 exlibris_path: str = EXLIBRIS_FOLDER):
        self.signed_copy_path = signed_copy_path
        self.exlibris_path = exlibris_path

    def get_attachment_statistics(self) -> Statistics:
        signed_copy_count = count_images_in_directory(self.signed_copy_path)
        ex_libris_count = count_images_in_directory(self.exlibris_path)

        return Statistics(
            albums_count=0,
            pages_count=0,
            purchase_price_count=0,
            deluxe_edition_count=0,
            signed_copies_count=signed_copy_count,
            ex_libris_count=ex_libris_count,
            place_of_purchase_pie=[]
        )
