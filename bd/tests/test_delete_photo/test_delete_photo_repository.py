import os
import tempfile
import unittest

from main.core.delete_photo.internal.photo_connexion import PhotoConnexion


class TestPhotoConnexion(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dedicace_folder = os.path.join(self.temp_dir.name, "dedicace")
        self.exlibris_folder = os.path.join(self.temp_dir.name, "exlibris")
        os.makedirs(self.dedicace_folder, exist_ok=True)
        os.makedirs(self.exlibris_folder, exist_ok=True)
        self.photo_connexion = PhotoConnexion(self.dedicace_folder, self.exlibris_folder)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_delete_dedicace_photo_exists_and_folder_empty(self):
        isbn = 12345
        photo_id = 1
        album_path = os.path.join(self.dedicace_folder, str(isbn))
        os.makedirs(album_path, exist_ok=True)
        photo_path = os.path.join(album_path, f"{photo_id}.jpeg")
        with open(photo_path, 'w') as f:
            f.write("test image content")

        result = self.photo_connexion.delete_dedicace(isbn, photo_id)

        self.assertFalse(os.path.exists(photo_path))
        self.assertFalse(os.path.exists(album_path))
        self.assertTrue(result)

    def test_delete_exlibris_photo_exists_and_folder_not_empty(self):
        isbn = 67890
        photo_id = 1
        album_path = os.path.join(self.exlibris_folder, str(isbn))
        os.makedirs(album_path, exist_ok=True)
        photo_path = os.path.join(album_path, f"{photo_id}.jpeg")
        with open(photo_path, 'w') as f:
            f.write("test image content")
        another_photo_path = os.path.join(album_path, f"{photo_id + 1}.jpeg")
        with open(another_photo_path, 'w') as f:
            f.write("another test image content")

        result = self.photo_connexion.delete_exlibris(isbn, photo_id)

        self.assertTrue(os.path.exists(photo_path))
        self.assertFalse(os.path.exists(another_photo_path))
        self.assertTrue(os.path.exists(album_path))
        self.assertTrue(result)

    def test_delete_photo_does_not_exist(self):
        isbn = 11111
        photo_id = 3
        album_path = os.path.join(self.dedicace_folder, str(isbn))
        os.makedirs(album_path, exist_ok=True)

        result = self.photo_connexion.delete_dedicace(isbn, photo_id)

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
