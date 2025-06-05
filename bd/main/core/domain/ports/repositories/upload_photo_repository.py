from abc import ABC, abstractmethod

from django.core.files.uploadedfile import UploadedFile


class UploadPhotoRepository(ABC):
    @abstractmethod
    def upload_photo(self, isbn: int, uploaded_file: UploadedFile, folder: str) -> bool:
        pass
