import os
import tempfile
import unittest

from main.core.infrastructure.persistence.file.delete_photo_adapter import DeleteDeletePhotoAdapter
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_PATH, EXLIBRIS_PATH


class TestPhotoConnexion(unittest.TestCase):

    def setUp(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        collection_id = 1

        cls.SIGNED_COPY_FOLDER = os.path.join(cls.temp_dir.name, SIGNED_COPY_PATH(collection_id))
        cls.EXLIBRIS_FOLDER = os.path.join(cls.temp_dir.name, EXLIBRIS_PATH(collection_id))

        os.makedirs(cls.SIGNED_COPY_FOLDER, exist_ok=True)
        os.makedirs(cls.EXLIBRIS_FOLDER, exist_ok=True)

        cls.photo_connexion = DeleteDeletePhotoAdapter()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_delete_dedicace_photo_exists_and_folder_empty(self):
        isbn = 12345
        photo_id = 1
        album_path = os.path.join(self.SIGNED_COPY_FOLDER, str(isbn))
        os.makedirs(album_path, exist_ok=True)
        photo_path = os.path.join(album_path, f"{photo_id}.jpeg")
        with open(photo_path, 'w') as f:
            f.write("test image content")

        result = self.photo_connexion.delete_photo(isbn, photo_id, self.SIGNED_COPY_FOLDER)

        self.assertFalse(os.path.exists(photo_path))
        self.assertFalse(os.path.exists(album_path))
        self.assertTrue(result)

    def test_delete_exlibris_photo_exists_and_folder_not_empty(self):
        isbn = 67890
        photo_id = 1
        album_path = os.path.join(self.EXLIBRIS_FOLDER, str(isbn))
        os.makedirs(album_path, exist_ok=True)
        photo_path = os.path.join(album_path, f"{photo_id}.jpeg")
        with open(photo_path, 'w') as f:
            f.write("test image content")
        another_photo_path = os.path.join(album_path, f"{photo_id + 1}.jpeg")
        with open(another_photo_path, 'w') as f:
            f.write("another test image content")

        result = self.photo_connexion.delete_photo(isbn, photo_id, self.EXLIBRIS_FOLDER)

        self.assertTrue(os.path.exists(photo_path))
        self.assertFalse(os.path.exists(another_photo_path))
        self.assertTrue(os.path.exists(album_path))
        self.assertTrue(result)

    def test_delete_photo_does_not_exist(self):
        isbn = 11111
        photo_id = 3
        album_path = os.path.join(self.SIGNED_COPY_FOLDER, str(isbn))
        os.makedirs(album_path, exist_ok=True)

        result = self.photo_connexion.delete_photo(isbn, photo_id, self.SIGNED_COPY_FOLDER)

        self.assertFalse(result)

    def test_renommer_photos(self):
        chemin_dossier = os.path.join(self.temp_dir.name, "renommer_test")
        os.makedirs(chemin_dossier, exist_ok=True)

        filenames = ["3.jpeg", "4.jpeg", "5.jpeg"]
        for i, filename in enumerate(filenames):
            with open(os.path.join(chemin_dossier, filename), 'w') as f:
                f.write(f"test image content {i + 1}")

        self.photo_connexion.renommer_photos(chemin_dossier)

        expected_files = ["1.jpeg", "2.jpeg", "3.jpeg"]
        actual_files = sorted(os.listdir(chemin_dossier))

        self.assertEqual(expected_files, actual_files)
        for i, filename in enumerate(expected_files):
            with open(os.path.join(chemin_dossier, filename), 'r') as f:
                content = f.read()
                self.assertEqual(f"test image content {i + 1}", content)


if __name__ == "__main__":
    unittest.main()
