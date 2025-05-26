import unittest
from pathlib import Path

from main.core.banner.banner_service import BannerService
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from test_banner.internal.banner_in_memory import BannerInMemory


class TestBannerService(unittest.TestCase):
    def setUp(self):
        self.repository = BannerInMemory()
        self.service = BannerService(self.repository)

    def test_main_no_images_returns_default_banner(self):
        # Arrange
        self.repository.images = []

        # Act
        result = self.service.main()

        # Assert
        self.assertTrue(self.repository.get_all_images_path_called)
        self.assertFalse(self.repository.get_random_attachment_called)
        self.assertIn('main/images/banner.jpg', result['banner_path'])
        self.assertEqual(0, result['banner_isbn'])
        self.assertEqual("", result['banner_type'])

    def test_main_with_images_calls_get_random_attachment(self):
        # Arrange
        self.repository.images = [
            "path/to/image1.jpg",
            "path/to/image2.jpg"
        ]
        self.repository.return_random_attachment = (
            "path/to/selected.jpg",
            "123456789",
            "dedicace"
        )

        # Act
        result = self.service.main()

        # Assert
        self.assertTrue(self.repository.get_all_images_path_called)
        self.assertTrue(self.repository.get_random_attachment_called)
        self.assertEqual("path/to/selected.jpg", result['banner_path'])
        self.assertEqual("123456789", result['banner_isbn'])
        self.assertEqual("dedicace", result['banner_type'])

    def test_main_verifies_correct_folders(self):
        # Act
        self.service.main()

        # Assert
        self.assertEqual(2, len(self.repository.last_paths_param))
        self.assertIn(SIGNED_COPY_FOLDER, self.repository.last_paths_param)
        self.assertIn(EXLIBRIS_FOLDER, self.repository.last_paths_param)

    def test_main_passes_images_to_get_random_attachment(self):
        # Arrange
        test_images = ["image1.jpg", "image2.jpg"]
        self.repository.images = test_images

        # Act
        self.service.main()

        # Assert
        self.assertEqual(test_images, self.repository.last_images_param)

    def test_main_handles_empty_path_from_random_attachment(self):
        # Arrange
        self.repository.images = ["image.jpg"]

        # Act
        result = self.service.main()
        # Assert
        self.assertEqual("", result['banner_path'])
        self.assertEqual(0, result['banner_isbn'])
        self.assertEqual("", result['banner_type'])

    def test_main_converts_path_to_string(self):
        # Arrange
        self.repository.images = ["image.jpg"]
        self.repository.return_random_attachment = (
            Path("path/to/image.jpg"),
            123456789,
            "exlibris"
        )

        # Act
        result = self.service.main()

        # Assert
        self.assertIsInstance(result['banner_path'], str)
        self.assertEqual("path/to/image.jpg", result['banner_path'])
        self.assertEqual(123456789, result['banner_isbn'])
        self.assertEqual("exlibris", result['banner_type'])

    def test_main_with_special_characters_in_paths(self):
        # Arrange
        self.repository.images = ["image with spaces.jpg"]
        self.repository.return_random_attachment = (
            "path/with spaces/and_special_chars#!@.jpg",
            "123456789",
            "dedicace"
        )

        # Act
        result = self.service.main()

        # Assert
        self.assertEqual(
            "path/with spaces/and_special_chars#!@.jpg",
            result['banner_path']
        )


if __name__ == '__main__':
    unittest.main()
