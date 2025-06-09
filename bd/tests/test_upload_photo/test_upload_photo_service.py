import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from main.core.application.usecases.upload_photo.upload_photo_service import UploadPhotoService
from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
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
        cls.collection_id = 1

    def test_correctly_upload_dedicace(self) -> None:
        is_uploaded = self.service.main(self.ISBN, self.uploaded_file, AttachmentType.SIGNED_COPY, self.collection_id)
        self.assertTrue(is_uploaded)
        self.assertEqual(SIGNED_COPY_FOLDER(self.collection_id), self.repository.type)

    def test_correctly_upload_exlibris(self) -> None:
        is_uploaded = self.service.main(self.ISBN, self.uploaded_file, AttachmentType.EXLIBRIS, self.collection_id)
        self.assertTrue(is_uploaded)
        self.assertEqual(EXLIBRIS_FOLDER(self.collection_id), self.repository.type)

    def test_incorrect_type(self) -> None:
        with self.assertRaises(ValueError):
            self.service.main(self.ISBN, self.uploaded_file, "incorrect type", self.collection_id)


if __name__ == '__main__':
    unittest.main()
