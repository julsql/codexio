import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.application.usecases.page_bd.page_bd_service import BdService
from main.core.domain.model.bd import BD
from main.core.domain.model.work_attachment import WorkAttachment
from main.core.domain.model.bd_with_attachment import BdWithAttachment
from tests.test_common.internal.logger_in_memory import LoggerInMemory
from tests.test_page_bd.internal.page_bd_in_memory import WorkAttachmentsInMemory, WorkDatabaseInMemory


class TestWorkService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_ISBN = 1234
        cls.TEST_BD_INFO = BD(
            isbn=cls.TEST_ISBN,
            title="Test Album",
            series="Test Series",
            number="1")

        cls.collection = 1

    def setUp(self) -> None:
        self.attachments_repository = WorkAttachmentsInMemory()
        self.database_repository = WorkDatabaseInMemory()
        self.logging_repository = LoggerInMemory()
        self.service = BdService(self.attachments_repository, self.database_repository, self.logging_repository)

    def test_main_with_existing_bd(self) -> None:
        # Arrange
        self.database_repository.add_bd(self.TEST_ISBN, self.TEST_BD_INFO)

        # Act
        result = self.service.main(self.TEST_ISBN, self.collection)

        # Assert
        self.assertEqual(BdWithAttachment(album=self.TEST_BD_INFO, attachments=WorkAttachment()), result)
        self.assertEqual(self.TEST_ISBN, self.attachments_repository.last_isbn)
        self.assertEqual(1, len(self.attachments_repository.added_attachments))

    def test_main_with_non_existing_bd(self) -> None:
        # Arrange
        non_existing_isbn = 5678

        # Act
        result = self.service.main(non_existing_isbn, self.collection)

        # Assert
        self.assertIsNone(result)
        self.assertIsNone(self.attachments_repository.last_isbn)
        self.assertEqual(0, len(self.attachments_repository.added_attachments))

    def test_main_with_database_error(self) -> None:
        # Arrange
        self.database_repository.set_error(True)

        # Act
        result = self.service.main(self.TEST_ISBN, self.collection)

        # Assert
        self.assertIsNone(result)
        self.assertIsNone(self.attachments_repository.last_isbn)
        self.assertEqual(0, len(self.attachments_repository.added_attachments))

    def test_main_with_multiple_calls(self) -> None:
        # Arrange
        test_data = [
            (1111, BD(isbn=1111, title="Album 1")),
            (2222, BD(isbn=2222, title="Album 2")),
            (3333, BD(isbn=3333, title="Album 3"))
        ]
        for isbn, info in test_data:
            self.database_repository.add_bd(isbn, info)

        # Act & Assert
        for isbn, expected_info in test_data:
            result = self.service.main(isbn, self.collection)
            self.assertEqual(BdWithAttachment(album=expected_info, attachments=WorkAttachment()), result)
            self.assertEqual(isbn, self.attachments_repository.last_isbn)

        self.assertEqual(len(test_data), len(self.attachments_repository.added_attachments))


if __name__ == '__main__':
    unittest.main()
