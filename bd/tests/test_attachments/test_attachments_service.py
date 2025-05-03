import unittest

from main.core.attachments.attachments_service import AttachmentsService
from main.core.common.data.data import SIGNED_COPY_FOLDER, EXLIBRIS_FOLDER, SIGNED_COPY_PATH, EXLIBRIS_PATH
from tests.test_attachments.internal.attachments_in_memory import AttachmentsInMemory


class TestAttachmentsService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = AttachmentsInMemory()
        cls.service = AttachmentsService(cls.repository)

    def test_main_signed_copies_empty(self) -> None:
        result = self.service.main_signed_copies()
        self.assertEqual({
            'attachments': [],
            'attachments_sum': 0,
            'title': 'dédicaces',
            'subtitle': 'dédicaces',
            'image_path': SIGNED_COPY_PATH
        }, result)

    def test_main_ex_libris_empty(self) -> None:
        result = self.service.main_ex_libris()
        self.assertEqual({
            'attachments': [],
            'attachments_sum': 0,
            'title': 'Ex-libris',
            'subtitle': 'ex-libris',
            'image_path': EXLIBRIS_PATH
        }, result)

    def test_main_signed_copies_with_data(self) -> None:
        test_data = [{'name': 'test.jpg', 'path': '/test/path'}]
        self.repository.attachments[SIGNED_COPY_FOLDER] = test_data

        result = self.service.main_signed_copies()
        self.assertEqual({
            'attachments': test_data,
            'attachments_sum': 1,
            'title': 'dédicaces',
            'subtitle': 'dédicaces',
            'image_path': SIGNED_COPY_PATH
        }, result)

    def test_main_ex_libris_with_data(self) -> None:
        test_data = [{'name': 'test.jpg', 'path': '/test/path'}]
        self.repository.attachments[EXLIBRIS_FOLDER] = test_data

        result = self.service.main_ex_libris()
        self.assertEqual({
            'attachments': test_data,
            'attachments_sum': 1,
            'title': 'Ex-libris',
            'subtitle': 'ex-libris',
            'image_path': EXLIBRIS_PATH
        }, result)


if __name__ == '__main__':
    unittest.main()
