from main.core.attachments.attachments_repository import AttachmentsRepository
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, SIGNED_COPY_PATH, EXLIBRIS_FOLDER, \
    EXLIBRIS_PATH


class AttachmentsService:

    def __init__(self, attachments_repository: AttachmentsRepository) -> None:
        self.repository = attachments_repository

    def main_signed_copies(self) -> dict[str, list[dict[str, str]] | int | str]:
        signed_copies, signed_copy_sum = self.repository.get_attachments(SIGNED_COPY_FOLDER)
        return {'attachments': signed_copies, 'attachments_sum': signed_copy_sum, 'title': 'dédicaces',
                'subtitle': 'dédicaces', 'image_path': SIGNED_COPY_PATH}

    def main_ex_libris(self) -> dict[str, list[dict[str, str]] | int | str]:
        exlibris, exlibris_sum = self.repository.get_attachments(EXLIBRIS_FOLDER)
        return {'attachments': exlibris, 'attachments_sum': exlibris_sum, 'title': 'Ex-libris', 'subtitle': 'ex-libris',
                'image_path': EXLIBRIS_PATH}
