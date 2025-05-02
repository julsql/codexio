import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.get_infos_service import GetInfosService
from tests.album_data_set import ASTERIX, ASTERIX_ISBN
from tests.test_add_album.internal.bd_in_memory import BdInMemory
from tests.test_add_album.internal.bd_in_memory_error import BdInMemoryError


class TestGetInfosService(unittest.TestCase):
    def setUp(self):
        # Repository avec informations complètes
        self.complete_repo = BdInMemory("complete", ASTERIX)

        partial_asterix1 = ASTERIX.copy()
        partial_asterix1["Couleurs"] = ""
        partial_asterix1["Édition"] = ""
        partial_asterix1["Date de publication"] = ""
        partial_asterix1["Synopsis"] = ""

        # Repository avec informations partielles
        self.partial_repo_1 = BdInMemory("partial1", partial_asterix1)

        partial_asterix2 = ASTERIX.copy()
        partial_asterix2["Album"] = ""
        partial_asterix2["Série"] = ""
        partial_asterix2["Numéro"] = ""
        partial_asterix2["Scénario"] = ""

        # Repository avec autres informations partielles
        self.partial_repo_2 = BdInMemory("partial2", partial_asterix2)

        # Repository qui lève une exception
        self.empty_repo = BdInMemory("error", {})
        self.error_repo = BdInMemoryError("error")

    def test_get_correct_info_successfully(self) -> None:
        self.service = GetInfosService([])
        self.service.isbn = 0
        info = self.service.corriger_info({})
        self.assertEqual({
            'Album': '', 'Couleurs': '', 'Date de publication': '',
            'Dessin': '', 'Édition': '', 'ISBN': '', 'Image': '',
            'Numéro': '', 'Pages': '', 'Prix': '', 'Scénario': '',
            'Synopsis': '', 'Série': '', 'Éditeur': ''},
            info)

    def test_complete_repository(self):
        """Test avec un repository contenant toutes les informations"""
        service = GetInfosService([self.complete_repo])
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertTrue(service.is_complete(result))
        self.assertEqual(result["Album"], ASTERIX["Album"])

    def test_complementary_repositories(self):
        """Test avec deux repositories qui se complètent"""
        service = GetInfosService([self.partial_repo_1, self.partial_repo_2])
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertTrue(service.is_complete(result))
        self.assertEqual(result["Album"], ASTERIX["Album"])
        self.assertEqual(result["Couleurs"], ASTERIX["Couleurs"])
        self.assertEqual(result["Synopsis"], ASTERIX["Synopsis"])

    def test_incomplete_repositories(self):
        """Test avec des repositories qui ne peuvent pas compléter toutes les informations"""
        service = GetInfosService([self.partial_repo_1])
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertFalse(service.is_complete(result))
        self.assertEqual(result["Synopsis"], "")

    def test_incomplete_repositories_on_error(self):
        """Test avec des repositories qui ne peuvent pas compléter toutes les informations dont un en erreur"""
        service = GetInfosService([self.partial_repo_1, self.error_repo])
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertFalse(service.is_complete(result))
        self.assertEqual(result["Synopsis"], "")

    def test_error_handling(self):
        """Test de la gestion des erreurs"""
        service = GetInfosService([self.empty_repo, self.complete_repo])
        result = service.main(ASTERIX_ISBN)

        self.assertIsNotNone(result)
        self.assertTrue(service.is_complete(result))
        self.assertEqual(result["Album"], ASTERIX["Album"])

    def test_empty_repositories_list(self):
        """Test avec une liste vide de repositories"""
        service = GetInfosService([])
        with self.assertRaises(AddAlbumError):
            service.main(ASTERIX_ISBN)

    def test_preserve_first_valid_value(self):
        """Test que les valeurs non vides ne sont pas écrasées"""
        repo1 = BdInMemory("repo1", {"Album": "Premier titre", 'ISBN': 1})
        repo2 = BdInMemory("repo2", {"Album": "Second titre", 'ISBN': 2})

        service = GetInfosService([repo1, repo2])
        result = service.main(1)

        self.assertEqual(result["Album"], "Premier titre")


if __name__ == '__main__':
    unittest.main()
