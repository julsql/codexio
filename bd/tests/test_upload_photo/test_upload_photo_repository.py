import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import django
from django.core.files.uploadedfile import SimpleUploadedFile

from main.core.upload_photo.internal.upload_photo_connexion import UploadPhotoConnexion
from main.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()


class TestUpdateDatabaseRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.ISBN = 1111
        cls.file_name = "test_file.jpeg"

        cls.SIGNED_COPY_FOLDER = os.path.join(cls.temp_dir.name, SIGNED_COPY_PATH)
        cls.EXLIBRIS_FOLDER = os.path.join(cls.temp_dir.name, EXLIBRIS_PATH)

        cls.repository = UploadPhotoConnexion()
        cls.file_content = b"Contenu du fichier exemple"
        cls.uploaded_file = SimpleUploadedFile(cls.file_name, cls.file_content, content_type="text/plain")

    def setUp(self) -> None:
        for root, dirs, files in os.walk(self.temp_dir.name, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)  # Supprimer les fichiers
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.rmdir(dir_path)  # Supprimer les répertoires vides

    def test_correctly_upload_dedicace(self) -> None:
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            is_uploaded = self.repository.upload_photo(self.ISBN, self.uploaded_file, self.SIGNED_COPY_FOLDER)
        self.assertTrue(is_uploaded)
        file = os.path.join(self.SIGNED_COPY_FOLDER, str(self.ISBN), "1.jpeg")
        self.assertTrue(os.path.exists(file))
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, self.file_content.decode('utf-8'))

    def test_correctly_upload_multiple_files(self) -> None:
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            is_uploaded = self.repository.upload_photo(self.ISBN, self.uploaded_file, self.SIGNED_COPY_FOLDER)
            is_uploaded = is_uploaded and self.repository.upload_photo(self.ISBN, self.uploaded_file,
                                                                       self.SIGNED_COPY_FOLDER)
        self.assertTrue(is_uploaded)
        folder = os.path.join(self.SIGNED_COPY_FOLDER, str(self.ISBN))
        self.assertEqual(2, len([f for f in Path(folder).iterdir() if f.is_file()]))

        file = os.path.join(folder, "1.jpeg")
        self.assertTrue(os.path.exists(file))
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, self.file_content.decode('utf-8'))

        file = os.path.join(folder, "2.jpeg")
        self.assertTrue(os.path.exists(file))
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, self.file_content.decode('utf-8'))

    def test_correctly_upload_multiple_files_and_delete(self) -> None:
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            is_uploaded = self.repository.upload_photo(self.ISBN, self.uploaded_file, self.SIGNED_COPY_FOLDER)
        self.assertTrue(is_uploaded)
        folder = os.path.join(self.SIGNED_COPY_FOLDER, str(self.ISBN))
        file = os.path.join(folder, "1.jpeg")
        self.assertTrue(os.path.exists(file))
        os.remove(file)
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            is_uploaded = self.repository.upload_photo(self.ISBN, self.uploaded_file, self.SIGNED_COPY_FOLDER)
        self.assertTrue(is_uploaded)
        folder = os.path.join(self.SIGNED_COPY_FOLDER, str(self.ISBN))
        file = os.path.join(folder, "1.jpeg")
        self.assertTrue(os.path.exists(file))

    def test_correctly_upload_exlilbris(self) -> None:
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            is_uploaded = self.repository.upload_photo(self.ISBN, self.uploaded_file, self.EXLIBRIS_FOLDER)
        self.assertTrue(is_uploaded)
        file = os.path.join(self.EXLIBRIS_FOLDER, str(self.ISBN), "1.jpeg")
        self.assertTrue(os.path.exists(file))
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, self.file_content.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
