import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from main.application.usecases.upload_photo.upload_photo_service import UploadPhotoService
from main.domain.model.attachment_type import AttachmentType
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from tests.test_upload_photo.internal.photo_in_memory import UploadPhotoInMemory


class TestUpdateDatabaseService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = UploadPhotoInMemory()
        cls.service = UploadPhotoService(cls.repository)
        cls.ISBN = 1111
        cls.file_name = "test_file.jpeg"
        cls.file_content = b"Contenu du fichier exemple"
        cls.uploaded_file = SimpleUploadedFile(cls.file_name, cls.file_content, content_type="text/plain")

    def test_correctly_upload_dedicace(self) -> None:
        is_uploaded = self.service.main(self.ISBN, self.uploaded_file, AttachmentType.SIGNED_COPY)
        self.assertTrue(is_uploaded)
        self.assertEqual(SIGNED_COPY_FOLDER, self.repository.type)

    def test_correctly_upload_exlibris(self) -> None:
        is_uploaded = self.service.main(self.ISBN, self.uploaded_file, AttachmentType.EXLIBRIS)
        self.assertTrue(is_uploaded)
        self.assertEqual(EXLIBRIS_FOLDER, self.repository.type)

    def test_incorrect_type(self) -> None:
        with self.assertRaises(ValueError):
            self.service.main(self.ISBN, self.uploaded_file, "incorrect type")


if __name__ == '__main__':
    unittest.main()
