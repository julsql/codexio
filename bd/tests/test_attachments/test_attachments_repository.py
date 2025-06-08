import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.domain.model.attachment import Attachment
from main.core.domain.model.attachments import Attachments
from main.core.infrastructure.persistence.file.attachments_adapter import AttachmentsAdapter
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH
from main.core.infrastructure.persistence.database.models.collection import Collection
from main.models import AppUser

from main.core.infrastructure.persistence.database.models.bd import BD


class TestAttachmentsConnexion(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=cls.user)

        cls.temp_dir = tempfile.TemporaryDirectory()

        # Création des chemins temporaires
        cls.SIGNED_COPY_FOLDER = os.path.join(cls.temp_dir.name, SIGNED_COPY_PATH(cls.collection.id))
        cls.EXLIBRIS_FOLDER = os.path.join(cls.temp_dir.name, EXLIBRIS_PATH(cls.collection.id))

        # Création des dossiers nécessaires
        os.makedirs(cls.SIGNED_COPY_FOLDER, exist_ok=True)
        os.makedirs(cls.EXLIBRIS_FOLDER, exist_ok=True)

        # Patch des chemins
        cls.paths_patcher = patch.multiple('main.core.infrastructure.persistence.file.paths',
                                           SIGNED_COPY_FOLDER=cls.SIGNED_COPY_FOLDER,
                                           EXLIBRIS_FOLDER=cls.EXLIBRIS_FOLDER)
        cls.paths_patcher.start()

        cls.repository = AttachmentsAdapter()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.paths_patcher.stop()
        cls.temp_dir.cleanup()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        # Nettoyage de la base de données avant chaque test
        BD.objects.filter(collection=self.collection).delete()

        # Nettoyage des dossiers temporaires
        for folder in [self.SIGNED_COPY_FOLDER, self.EXLIBRIS_FOLDER]:
            for root, dirs, files in os.walk(folder, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    def create_test_files(self, folder: str, isbn: int, nb_files: int) -> None:
        album_folder = os.path.join(folder, str(isbn))
        os.makedirs(album_folder, exist_ok=True)
        for i in range(1, nb_files + 1):
            with open(os.path.join(album_folder, f"{i}.jpeg"), 'w') as f:
                f.write("test content")

    def test_get_attachments_empty_folder(self) -> None:
        attachments = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)
        self.assertEqual(Attachments([]), attachments)
        self.assertEqual(0, attachments.sum)

    def test_get_attachments_with_files_no_bd_entry(self) -> None:
        test_isbn = 1234
        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, 2)

        attachments = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)

        self.assertEqual(1, len(attachments.attachments_list))
        self.assertEqual(2, attachments.sum)
        self.assertEqual(Attachment(isbn=test_isbn, title="", number="", series="", total=2),
                         attachments.attachments_list[0])

    def test_get_attachments_with_files_and_bd_entry(self) -> None:
        test_isbn = 5678
        test_bd = {
            'isbn': test_isbn,
            'album': "Test Album",
            'number': "1",
            'series': "Test Series",
            "deluxe_edition": True
        }
        BD.objects.create(**test_bd,
                          collection=self.collection)
        self.create_test_files(self.SIGNED_COPY_FOLDER, test_isbn, 3)

        attachments = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)

        self.assertEqual(1, len(attachments.attachments_list))
        self.assertEqual(3, attachments.sum)
        self.assertEqual(Attachment(isbn=test_isbn, title="Test Album", number="1", series="Test Series", total=3),
                         attachments.attachments_list[0])

    def test_get_attachments_multiple_albums(self) -> None:
        test_data = [
            {"isbn": 1111, "album": "Album 1", "number": "1", "series": "Series 1", "deluxe_edition": True},
            {"isbn": 2222, "album": "Album 2", "number": "2", "series": "Series 2", "deluxe_edition": True}
        ]

        for data in test_data:
            BD.objects.create(**data, collection=self.collection)
            self.create_test_files(self.SIGNED_COPY_FOLDER, data['isbn'], 2)

        attachments = self.repository.get_attachments(self.SIGNED_COPY_FOLDER)

        self.assertEqual(2, len(attachments.attachments_list))
        self.assertEqual(4, attachments.sum)
        for i, data in enumerate(test_data):
            self.assertEqual(
                Attachment(isbn=data['isbn'], title=data['album'], number=data['number'], series=data['series'],
                           total=2), next(
                    (item for item in attachments.attachments_list if item.isbn == data['isbn']), None))

        if __name__ == '__main__':
            unittest.main()
