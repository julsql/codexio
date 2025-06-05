import unittest

from main.core.application.usecases.add_album.get_infos_service import GetInfosService
from main.core.domain.exceptions.album_exceptions import AlbumNotFoundException
from main.core.domain.model.album import Album
from tests.album_data_set import ASTERIX
from tests.test_add_album.album_large_data_set import ASTERIX_ISBN
from tests.test_add_album.internal.bd_in_memory import BdInMemory
from tests.test_add_album.internal.bd_in_memory_error import BdInMemoryError
from tests.test_common.internal.logger_in_memory import LoggerInMemory


class TestGetInfosService(unittest.TestCase):
    def setUp(self):
        self.logging_repository = LoggerInMemory()
        # Repository avec informations complètes
        self.complete_repo = BdInMemory("complete", ASTERIX)

        partial_asterix1 = ASTERIX.copy()
        partial_asterix1.colorist = ""
        partial_asterix1.edition = ""
        partial_asterix1.publication_date = ""
        partial_asterix1.synopsis = ""

        # Repository avec informations partielles
        self.partial_repo_1 = BdInMemory("partial1", partial_asterix1)

        partial_asterix2 = ASTERIX.copy()
        partial_asterix2.title = ""
        partial_asterix2.series = ""
        partial_asterix2.number = ""
        partial_asterix2.writer = ""

        # Repository avec autres informations partielles
        self.partial_repo_2 = BdInMemory("partial2", partial_asterix2)

        # Repository qui lève une exception
        self.empty_repo = BdInMemory("error", Album(isbn=0))
        self.error_repo = BdInMemoryError("error")

    def test_complete_repository(self):
        """Test avec un repository contenant toutes les informations"""
        service = GetInfosService([self.complete_repo], self.logging_repository)
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertTrue(result.is_complete())
        self.assertEqual(result.title, ASTERIX.title)

    def test_complementary_repositories(self):
        """Test avec deux repositories qui se complètent"""
        service = GetInfosService([self.partial_repo_1, self.partial_repo_2], self.logging_repository)
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertTrue(result.is_complete())
        self.assertEqual(result.title, ASTERIX.title)
        self.assertEqual(result.colorist, ASTERIX.colorist)
        self.assertEqual(result.synopsis, ASTERIX.synopsis)

    def test_incomplete_repositories(self):
        """Test avec des repositories qui ne peuvent pas compléter toutes les informations"""
        service = GetInfosService([self.partial_repo_1], self.logging_repository)
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertFalse(result.is_complete())
        self.assertEqual(result.synopsis, "")

    def test_incomplete_repositories_on_error(self):
        """Test avec des repositories qui ne peuvent pas compléter toutes les informations dont un en erreur"""
        service = GetInfosService([self.partial_repo_1, self.error_repo], self.logging_repository)
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertFalse(result.is_complete())
        self.assertEqual(result.synopsis, "")

    def test_error_handling(self):
        """Test de la gestion des erreurs"""
        service = GetInfosService([self.empty_repo, self.complete_repo], self.logging_repository)
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertTrue(result.is_complete())
        self.assertEqual(result.title, ASTERIX.title)

    def test_empty_repositories_list(self):
        """Test avec une liste vide de repositories"""
        service = GetInfosService([], self.logging_repository)
        with self.assertRaises(AlbumNotFoundException):
            service.main(ASTERIX_ISBN)

    def test_preserve_first_valid_value(self):
        """Test que les valeurs non vides ne sont pas écrasées"""
        album1 = Album(title="Premier titre", isbn=1)
        album2 = Album(title="Second titre", isbn=2)
        repo1 = BdInMemory("repo1", album1)
        repo2 = BdInMemory("repo2", album2)

        service = GetInfosService([repo1, repo2], self.logging_repository)
        result = service.main(1)

        self.assertEqual(result.title, "Premier titre")


if __name__ == '__main__':
    unittest.main()
