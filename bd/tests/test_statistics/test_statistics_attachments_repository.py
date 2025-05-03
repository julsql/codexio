import os
import sys
import tempfile
import unittest

import django

from main.core.common.data.data import SIGNED_COPY_PATH, EXLIBRIS_PATH

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.statistics.internal.statistics_attachments_connexion import StatisticsAttachmentsConnexion


class TestStatisticsAttachmentsConnexion(unittest.TestCase):

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

        cls.repository = StatisticsAttachmentsConnexion(cls.SIGNED_COPY_FOLDER, cls.EXLIBRIS_FOLDER)

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

    def create_test_files(self, folder: str, isbn: str, filenames: list[str]) -> None:
        album_folder = os.path.join(folder, str(isbn))
        os.makedirs(album_folder, exist_ok=True)
        for filename in filenames:
            with open(os.path.join(album_folder, filename), 'w') as f:
                f.write("test content")

    def test_get_information_empty_database(self) -> None:
        # Act
        result = self.repository.get_information()

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual({'dedicaces': 0, 'exlibris': 0}, result)

    def test_get_information_with_data(self) -> None:
        # Arrange
        self.create_test_files(self.SIGNED_COPY_FOLDER, "123456789", ["1.jpeg", "2.jpeg", "3.jpeg"])
        self.create_test_files(self.SIGNED_COPY_FOLDER, "987654321", ["1.jpeg", "2.jpeg"])

        self.create_test_files(self.EXLIBRIS_FOLDER, "123456789", ["1.jpeg"])
        self.create_test_files(self.EXLIBRIS_FOLDER, "987654321", ["1.jpeg", "2.jpeg"])

        # Act
        result = self.repository.get_information()

        # Assert
        self.assertEqual({
            'dedicaces': 5,  # 2 + 3
            'exlibris': 3,  # 1 + 2
        }, result)

    def test_get_information_with_zero_attachments(self) -> None:
        # Arrange
        self.create_test_files(self.SIGNED_COPY_FOLDER, "123456789", [])

        # Act
        result = self.repository.get_information()

        # Assert
        self.assertEqual({
            'dedicaces': 0,
            'exlibris': 0
        }, result)


if __name__ == '__main__':
    unittest.main()
