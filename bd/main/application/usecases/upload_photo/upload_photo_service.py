from django.core.files.uploadedfile import UploadedFile

from main.domain.model.attachment_type import AttachmentType
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER


class UploadPhotoService:
    def __init__(self, photo_repository) -> None:
        self.repository = photo_repository

    def main(self, isbn: int, uploaded_file: UploadedFile, photo_type: AttachmentType) -> bool:
        if photo_type == AttachmentType.SIGNED_COPY:
            return self.repository.upload_photo(isbn, uploaded_file, SIGNED_COPY_FOLDER)
        elif photo_type == AttachmentType.EXLIBRIS:
            return self.repository.upload_photo(isbn, uploaded_file, EXLIBRIS_FOLDER)
        else:
            raise ValueError('Unknown photo type')
