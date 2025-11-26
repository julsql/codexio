from abc import ABC

from django.core.files.uploadedfile import UploadedFile

from main.core.domain.ports.repositories.upload_photo_repository import UploadPhotoRepository


class UploadPhotoInMemory(UploadPhotoRepository, ABC):
    type = ""

    def upload_photo(self, isbn: int, uploaded_file: UploadedFile, folder: str) -> bool:
        self.type = folder
        return True
