import os
import sys
import tempfile
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH
from main.infrastructure.persistence.file.page_bd_attachments_adapter import PageBdAttachmentsAdapter


class TestPageBdAttachmentsConnexion(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.temp_dir = tempfile.TemporaryDirectory()

        # Création des chemins temporaires
        cls.SIGNED_COPY_FOLDER = os.path.join(cls.temp_dir.name, SIGNED_COPY_PATH)
        cls.EXLIBRIS_FOLDER = os.path.join(cls.temp_dir.name, EXLIBRIS_PATH)

        # Création des dossiers nécessaires
        os.makedirs(cls.SIGNED_COPY_FOLDER, exist_ok=True)
        os.makedirs(cls.EXLIBRIS_FOLDER, exist_ok=True)

        cls.repository = PageBdAttachmentsAdapter(cls.SIGNED_COPY_FOLDER, cls.EXLIBRIS_FOLDER)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        # Nettoyage des dossiers temporaires
        for folder in [self.SIGNED_COPY_FOLDER, self.EXLIBRIS_FOLDER]:
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    def create_test_files(self, folder: str, isbn: int, filenames: list[str]) -> None:
        album_folder = os.path.join(folder, str(isbn))
        os.makedirs(album_folder, exist_ok=True)
        for filename in filenames:
            with open(os.path.join(album_folder, filename), 'w') as f:
                f.write("test content")

    def test_add_attachments_empty_folders(self) -> None:
        test_isbn = 1234

        result = self.repository.get_attachments(test_isbn)

        self.assertEqual([], result.dedicaces)
        self.assertEqual([], result.ex_libris)

    def test_add_attachments_with_dedicaces_only(self) -> None:
        test_isbn = 1234
        test_files = ["1.jpeg", "2.jpeg", "3.jpeg"]

        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, test_files)
        result = self.repository.get_attachments(test_isbn)

        self.assertEqual(sorted(test_files), result.dedicaces)
        self.assertEqual([], result.ex_libris)

    def test_add_attachments_with_exlibris_only(self) -> None:
        test_isbn = 1234
        test_files = ["1.jpeg", "2.jpeg"]

        self.create_test_files(self.EXLIBRIS_FOLDER, test_isbn, test_files)

        result = self.repository.get_attachments(test_isbn)

        self.assertEqual([], result.dedicaces)
        self.assertEqual(sorted(test_files), result.ex_libris)

    def test_add_attachments_with_both_types(self) -> None:
        test_isbn = 1234
        dedicace_files = ["1.jpeg", "2.jpeg"]
        exlibris_files = ["1.jpeg", "2.jpeg", "3.jpeg"]

        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, dedicace_files)
        self.create_test_files(self.EXLIBRIS_FOLDER, test_isbn, exlibris_files)

        result = self.repository.get_attachments(test_isbn)

        self.assertEqual(sorted(dedicace_files), result.dedicaces)
        self.assertEqual(sorted(exlibris_files), result.ex_libris)

    def test_add_attachments_ignore_non_jpeg(self) -> None:
        test_isbn = 1234
        test_files = ["1.jpeg", "2.txt", "3.png", "4.jpeg"]

        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, test_files)

        result = self.repository.get_attachments(test_isbn)

        expected_files = ["1.jpeg", "4.jpeg"]
        self.assertEqual(expected_files, result.dedicaces)

    def test_attachment_album_non_existent_folder(self) -> None:
        test_isbn = 1234
        result = self.repository.attachment_album(test_isbn, self.SIGNED_COPY_FOLDER)
        self.assertEqual([], result)

    def test_get_photo_dossier_non_existent_path(self) -> None:
        result = self.repository.get_photo_dossier("/non/existent/path")
        self.assertEqual([], result)

    def test_get_photo_dossier_not_a_directory(self) -> None:
        with open(os.path.join(self.temp_dir.name, "test.txt"), 'w') as f:
            f.write("test")
        result = self.repository.get_photo_dossier(os.path.join(self.temp_dir.name, "test.txt"))
        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()
