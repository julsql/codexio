from django.core.files.uploadedfile import UploadedFile


class UploadPhotoService:
    def __init__(self, photo_repository):
        self.repository = photo_repository

    def main(self, isbn: int, uploaded_file: UploadedFile, photo_type: str) -> bool:
        if photo_type == 'dedicaces':
            return self.repository.upload_dedicaces(isbn, uploaded_file)
        else:
            return self.repository.upload_exlibris(isbn, uploaded_file)
