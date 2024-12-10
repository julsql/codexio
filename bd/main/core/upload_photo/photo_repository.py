from abc import ABC, abstractmethod

from django.core.files.uploadedfile import UploadedFile


class PhotoRepository(ABC):
    @abstractmethod
    def upload_dedicace(self, isbn: int, uploaded_file: UploadedFile) -> bool:
        pass

    @abstractmethod
    def upload_exlibris(self, isbn: int, uploaded_file: UploadedFile) -> bool:
        pass
