import unittest

from main.application.usecases.random_attachment.random_attachment_service import RandomAttachmentService
from main.domain.model.attachment_type import AttachmentType
from main.domain.model.random_attachment import RandomAttachment
from main.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER
from test_random_attachment.internal.random_attachment_in_memory import RandomAttachmentInMemory


class TestRandomAttachmentService(unittest.TestCase):
    def setUp(self):
        self.repository = RandomAttachmentInMemory()
        self.service = RandomAttachmentService(self.repository)

    def test_main_no_images_returns_default_banner(self):
        # Arrange
        self.repository.images = []

        # Act
        banner = self.service.main()

        # Assert
        self.assertTrue(self.repository.get_all_images_path_called)
        self.assertFalse(self.repository.get_random_attachment_called)
        self.assertIn('main/images/random_attachment.jpg', banner.path)
        self.assertEqual(0, banner.isbn)
        self.assertIsNone(banner.type)

    def test_main_with_images_calls_get_random_attachment(self):
        # Arrange
        self.repository.images = [
            "path/to/image1.jpg",
            "path/to/image2.jpg"
        ]
        self.repository.return_random_attachment = RandomAttachment(
            path="path/to/selected.jpg",
            isbn=123456789,
            type=AttachmentType.SIGNED_COPY
        )

        # Act
        banner = self.service.main()

        # Assert
        self.assertTrue(self.repository.get_all_images_path_called)
        self.assertTrue(self.repository.get_random_attachment_called)
        self.assertEqual("path/to/selected.jpg", banner.path)
        self.assertEqual(123456789, banner.isbn)
        self.assertEqual(AttachmentType.SIGNED_COPY, banner.type)

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
        banner = self.service.main()

        # Assert
        self.assertEqual("", banner.path)
        self.assertEqual(0, banner.isbn)
        self.assertIsNone(banner.type)

    def test_main_converts_path_to_string(self):
        # Arrange
        self.repository.images = ["image.jpg"]
        self.repository.return_random_attachment = RandomAttachment(
            path="path/to/image.jpg",
            isbn=123456789,
            type=AttachmentType.EXLIBRIS
        )

        # Act
        banner = self.service.main()

        # Assert
        self.assertIsInstance(banner.path, str)
        self.assertEqual("path/to/image.jpg", banner.path)
        self.assertEqual(123456789, banner.isbn)
        self.assertEqual(AttachmentType.EXLIBRIS, banner.type)

    def test_main_with_special_characters_in_paths(self):
        # Arrange
        self.repository.images = ["image with spaces.jpg"]
        self.repository.return_random_attachment = RandomAttachment(
            path="path/with spaces/and_special_chars#!@.jpg",
            isbn=123456789,
            type=AttachmentType.SIGNED_COPY
        )

        # Act
        banner = self.service.main()

        # Assert
        self.assertEqual(
            "path/with spaces/and_special_chars#!@.jpg",
            banner.path
        )


if __name__ == '__main__':
    unittest.main()
