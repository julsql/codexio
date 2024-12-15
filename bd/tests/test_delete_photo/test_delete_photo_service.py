import unittest

from django.core.files.uploadedfile import SimpleUploadedFile

from main.core.delete_photo.delete_photo_service import DeletePhotoService
from tests.test_delete_photo.internal.photo_in_memory import PhotoInMemory


class TestDeletePhotoService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = PhotoInMemory()
        cls.service = DeletePhotoService(cls.repository)
        cls.ISBN = 1111
        cls.file_name = "1.jpeg"
        cls.file_content = b"Contenu du fichier exemple"
        cls.uploaded_file = SimpleUploadedFile(cls.file_name, cls.file_content, content_type="text/plain")

    def test_correctly_delete_dedicace(self) -> None:
        is_uploaded = self.service.main(self.ISBN, 1, "dedicaces")
        self.assertTrue(is_uploaded)
        self.assertEqual("dedicaces", self.repository.type)

    def test_correctly_delete_exlibris(self) -> None:
        is_uploaded = self.service.main(self.ISBN, 1, "exlibris")
        self.assertTrue(is_uploaded)
        self.assertEqual("exlibris", self.repository.type)

    def test_incorrect_type(self) -> None:
        with self.assertRaises(ValueError):
            self.service.main(self.ISBN, 1, "incorrect type")


if __name__ == '__main__':
    unittest.main()
