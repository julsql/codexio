from django.core.files.uploadedfile import UploadedFile


class UploadPhotoService:
    def __init__(self, photo_repository) -> None:
        self.repository = photo_repository

    def main(self, isbn: int, uploaded_file: UploadedFile, photo_type: str) -> bool:
        if photo_type == 'dedicaces':
            return self.repository.upload_dedicace(isbn, uploaded_file)
        elif photo_type == 'exlibris':
            return self.repository.upload_exlibris(isbn, uploaded_file)
        else:
            raise ValueError('Unknown photo type')
