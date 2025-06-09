import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from main.core.application.usecases.delete_photo.delete_photo_service import DeletePhotoService
from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.persistence.file.paths import EXLIBRIS_FOLDER, SIGNED_COPY_FOLDER
from tests.test_delete_photo.internal.photo_in_memory import DeletePhotoInMemory


class TestDeletePhotoService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = DeletePhotoInMemory()
        cls.service = DeletePhotoService(cls.repository)
        cls.ISBN = 1111
        cls.file_name = "1.jpeg"
        cls.file_content = b"Contenu du fichier exemple"
        cls.uploaded_file = SimpleUploadedFile(cls.file_name, cls.file_content, content_type="text/plain")
        cls.collection_id = 1

    def test_correctly_delete_dedicace(self) -> None:
        is_uploaded = self.service.main(self.ISBN, 1, AttachmentType.SIGNED_COPY, self.collection_id)
        self.assertTrue(is_uploaded)
        self.assertEqual(SIGNED_COPY_FOLDER(self.collection_id), self.repository.type)

    def test_correctly_delete_exlibris(self) -> None:
        is_uploaded = self.service.main(self.ISBN, 1, AttachmentType.EXLIBRIS, self.collection_id)
        self.assertTrue(is_uploaded)
        self.assertEqual(EXLIBRIS_FOLDER(self.collection_id), self.repository.type)

    def test_incorrect_type(self) -> None:
        with self.assertRaises(ValueError):
            self.service.main(self.ISBN, 1, "incorrect type", self.collection_id)


if __name__ == '__main__':
    unittest.main()
