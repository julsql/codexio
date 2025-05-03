import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.common.database.internal.bd_model import BD
from main.core.common.data.data import SIGNED_COPY_PATH, EXLIBRIS_PATH
from main.core.attachments.internal.attachments_connexion import AttachmentsConnexion


class TestAttachmentsConnexion(unittest.TestCase):

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

        # Patch des chemins
        cls.paths_patcher = patch.multiple('main.core.common.data.data',
                                           SIGNED_COPY_FOLDER=cls.SIGNED_COPY_FOLDER,
                                           EXLIBRIS_FOLDER=cls.EXLIBRIS_FOLDER)
        cls.paths_patcher.start()

        cls.repository = AttachmentsConnexion()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.paths_patcher.stop()
        cls.temp_dir.cleanup()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        # Nettoyage de la base de données avant chaque test
        BD.objects.all().delete()

        # Nettoyage des dossiers temporaires
        for folder in [self.SIGNED_COPY_FOLDER, self.EXLIBRIS_FOLDER]:
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    def create_test_files(self, folder: str, isbn: str, nb_files: int) -> None:
        album_folder = os.path.join(folder, str(isbn))
        os.makedirs(album_folder, exist_ok=True)
        for i in range(1, nb_files + 1):
            with open(os.path.join(album_folder, f"{i}.jpeg"), 'w') as f:
                f.write("test content")

    def test_get_attachments_empty_folder(self) -> None:
        attachments, total = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)
        self.assertEqual([], attachments)
        self.assertEqual(0, total)

    def test_get_attachments_with_files_no_bd_entry(self) -> None:
        test_isbn = "1234"
        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, 2)

        attachments, total = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)

        self.assertEqual(1, len(attachments))
        self.assertEqual(2, total)
        self.assertEqual({
            'isbn': test_isbn,
            'album': "",
            'number': "",
            'series': "",
            'range': range(1, 3),
            'attachments': 2
        }, attachments[0])

    def test_get_attachments_with_files_and_bd_entry(self) -> None:
        test_isbn = "5678"
        test_bd = {
            'isbn': test_isbn,
            'album': "Test Album",
            'number': "1",
            'series': "Test Series",
            "deluxe_edition": True
        }
        BD.objects.create(**test_bd)
        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, 3)

        attachments, total = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)

        self.assertEqual(1, len(attachments))
        self.assertEqual(3, total)
        self.assertEqual({
            'isbn': test_isbn,
            'album': "Test Album",
            'number': "1",
            'series': "Test Series",
            'range': range(1, 4),
            'attachments': 3
        }, attachments[0])

    def test_get_attachments_multiple_albums(self) -> None:
        test_data = [
            {"isbn": "1111", "album": "Album 1", "number": "1", "series": "Series 1", "deluxe_edition": True},
            {"isbn": "2222", "album": "Album 2", "number": "2", "series": "Series 2", "deluxe_edition": True}
        ]

        for data in test_data:
            BD.objects.create(**data)
            self.create_test_files(self.SIGNED_COPY_FOLDER, data['isbn'], 2)

        attachments, total = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)

        self.assertEqual(2, len(attachments))
        self.assertEqual(4, total)
        for i, data in enumerate(test_data):
            self.assertEqual({
                'isbn': data['isbn'],
                'album': data['album'],
                'number': data['number'],
                'series': data['series'],
                'range': range(1, 3),
                'attachments': 2
            }, next((item for item in attachments if item["isbn"] == data['isbn']), None))


if __name__ == '__main__':
    unittest.main()
