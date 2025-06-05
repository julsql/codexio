import unittest

from main.core.application.usecases.attachments.attachments_service import AttachmentsService
from main.core.domain.model.attachment import Attachment
from main.core.domain.model.attachments import Attachments
from main.core.infrastructure.persistence.file import SIGNED_COPY_PATH, EXLIBRIS_PATH, SIGNED_COPY_FOLDER, \
    EXLIBRIS_FOLDER
from tests.test_attachments.internal.attachments_in_memory import AttachmentsInMemory


class TestAttachmentsService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = AttachmentsInMemory()
        cls.service = AttachmentsService(cls.repository)

    def test_main_signed_copies_empty(self) -> None:
        result = self.service.main_signed_copies()
        self.assertEqual(
            Attachments(attachments_list=[], title="dédicaces", subtitle="dédicaces", image_path=SIGNED_COPY_PATH),
            result)

    def test_main_ex_libris_empty(self) -> None:
        result = self.service.main_ex_libris()
        self.assertEqual(
            Attachments(attachments_list=[], title="Ex-libris", subtitle="ex-libris", image_path=EXLIBRIS_PATH), result)

    def test_main_signed_copies_with_data(self) -> None:
        test_data = [Attachment(isbn=0, title="Titre de test", number="1", series="Série de test", total=2)]
        self.repository.attachments[SIGNED_COPY_FOLDER] = test_data

        result = self.service.main_signed_copies()
        self.assertEqual(
            Attachments(attachments_list=test_data, title="dédicaces", subtitle="dédicaces",
                        image_path=SIGNED_COPY_PATH), result)

    def test_main_ex_libris_with_data(self) -> None:
        test_data = [Attachment(isbn=0, title="Titre de test", number="1", series="Série de test", total=2)]
        self.repository.attachments[EXLIBRIS_FOLDER] = test_data

        result = self.service.main_ex_libris()
        self.assertEqual(
            Attachments(attachments_list=test_data, title="Ex-libris", subtitle="ex-libris", image_path=EXLIBRIS_PATH),
            result)


if __name__ == '__main__':
    unittest.main()
