from main.core.attachments.attachments_repository import AttachmentsRepository


class AttachmentsService:
    SIGNED_COPY_PATH = "main/images/dedicaces"
    EX_LIBRIS_PATH = "main/images/exlibris"

    def __init__(self, attachments_repository: AttachmentsRepository) -> None:
        self.repository = attachments_repository

    def main_signed_copies(self) -> dict[str, list[dict[str, str]] | int | str]:
        signed_copies, signed_copy_sum = self.repository.get_attachments(self.SIGNED_COPY_PATH)
        return {'attachments': signed_copies, 'attachments_sum': signed_copy_sum, 'title': 'dédicaces',
                'subtitle': 'dédicaces', 'image_path': self.SIGNED_COPY_PATH}

    def main_ex_libris(self) -> dict[str, list[dict[str, str]] | int | str]:
        exlibris, exlibris_sum = self.repository.get_attachments(self.EX_LIBRIS_PATH)
        return {'attachments': exlibris, 'attachments_sum': exlibris_sum, 'title': 'Ex-libris', 'subtitle': 'ex-libris',
                'image_path': self.EX_LIBRIS_PATH}
