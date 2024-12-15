from abc import ABC

from django.core.files.uploadedfile import UploadedFile

from main.core.upload_photo.photo_repository import PhotoRepository


class PhotoInMemory(PhotoRepository, ABC):
    type = ""

    def upload_dedicace(self, isbn: int, uploaded_file: UploadedFile) -> bool:
        self.type = "dedicaces"
        return True

    def upload_exlibris(self, isbn: int, uploaded_file: UploadedFile) -> bool:
        self.type = "exlibris"
        return True
