import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.application.usecases.attachments.attachments_service import AttachmentsService
from main.core.domain.model.attachment import Attachment
from main.core.domain.model.attachments import Attachments
from main.core.infrastructure.persistence.database.models.collection import Collection
from main.core.infrastructure.persistence.file.paths import SIGNED_COPY_FOLDER, EXLIBRIS_PATH, SIGNED_COPY_PATH, \
    EXLIBRIS_FOLDER
from main.models import AppUser
from tests.test_attachments.internal.attachments_in_memory import AttachmentsInMemory


class TestAttachmentsService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = AttachmentsInMemory()
        cls.service = AttachmentsService(cls.repository)

        cls.user = AppUser.objects.get(username="admin")
        cls.collection = Collection.objects.get(accounts=cls.user)

        # Création des chemins temporaires
        cls.SIGNED_COPY_FOLDER = SIGNED_COPY_PATH(cls.collection.id)
        cls.EXLIBRIS_FOLDER = EXLIBRIS_PATH(cls.collection.id)

    def test_main_signed_copies_empty(self) -> None:
        result = self.service.main_signed_copies(self.collection.id)
        self.assertEqual(
            Attachments(attachments_list=[],
                        title="dédicaces",
                        subtitle="Toutes les dédicaces",
                        type="dédicace",
                        image_path=self.SIGNED_COPY_FOLDER),
            result)

    def test_main_ex_libris_empty(self) -> None:
        result = self.service.main_ex_libris(self.collection.id)
        self.assertEqual(
            Attachments(attachments_list=[],
                        title="Ex-libris",
                        subtitle="Tous les ex-libris",
                        type="ex-libris",
                        image_path=self.EXLIBRIS_FOLDER),
            result)

    def test_main_signed_copies_with_data(self) -> None:
        test_data = [Attachment(isbn=0, title="Titre de test", number="1", series="Série de test", total=2)]
        self.repository.attachments[SIGNED_COPY_FOLDER(self.collection.id)] = test_data

        result = self.service.main_signed_copies(self.collection.id)
        self.assertEqual(
            Attachments(attachments_list=test_data,
                        title="dédicaces",
                        subtitle="Toutes les dédicaces",
                        type="dédicace",
                        image_path=self.SIGNED_COPY_FOLDER),
            result)

    def test_main_ex_libris_with_data(self) -> None:
        test_data = [Attachment(isbn=0, title="Titre de test", number="1", series="Série de test", total=2)]
        self.repository.attachments[EXLIBRIS_FOLDER(self.collection.id)] = test_data

        result = self.service.main_ex_libris(self.collection.id)
        self.assertEqual(
            Attachments(attachments_list=test_data,
                        title="Ex-libris",
                        subtitle="Tous les ex-libris",
                        type="ex-libris",
                        image_path=self.EXLIBRIS_FOLDER),
            result)


if __name__ == '__main__':
    unittest.main()
