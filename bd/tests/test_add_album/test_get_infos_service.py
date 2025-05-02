import unittest

from main.core.add_album.add_album_error import AddAlbumError
from main.core.add_album.get_infos_service import GetInfosService
from test_add_album.internal.bd_in_memory import BdInMemory
from test_add_album.internal.bd_in_memory_error import BdInMemoryError


class TestGetInfosService(unittest.TestCase):
    def setUp(self):
        # Repository avec informations complètes
        self.complete_repo = BdInMemory("complete", {
            "Album": "Astérix",
            "Série": "Astérix",
            "Numéro": "1",
            "Scénario": "René Goscinny",
            "Dessin": "Albert Uderzo",
            "Couleurs": "Albert Uderzo",
            "Éditeur": "Dargaud",
            "Édition": "Les Éditions Albert René",
            "Date de publication": "2023-01-01",
            "Pages": "48",
            "Prix": 10,
            "Synopsis": "Les aventures d'Astérix",
            "Image": "url_image.jpg"
        })

        # Repository avec informations partielles
        self.partial_repo_1 = BdInMemory("partial1", {
            "Album": "Astérix",
            "Série": "Astérix",
            "Numéro": "1",
            "Scénario": "René Goscinny",
            "Dessin": "Albert Uderzo",
            "Couleurs": "",  # Manquant
            "Éditeur": "Dargaud",
            "Édition": "",  # Manquant
            "Date de publication": "",  # Manquant
            "Pages": "48",
            "Prix": 10,
            "Synopsis": "",  # Manquant
            "Image": "url_image.jpg"
        })

        # Repository avec autres informations partielles
        self.partial_repo_2 = BdInMemory("partial2", {
            "Album": "",  # Manquant
            "Série": "",  # Manquant
            "Numéro": "",  # Manquant
            "Scénario": "",  # Manquant
            "Dessin": "Albert Uderzo",
            "Couleurs": "Albert Uderzo",
            "Éditeur": "Dargaud",
            "Édition": "Les Éditions Albert René",
            "Date de publication": "2023-01-01",
            "Pages": "48",
            "Prix": 10,
            "Synopsis": "Les aventures d'Astérix",
            "Image": "url_image2.jpg"
        })

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
        result = service.main(123)

        self.assertIsNotNone(result)
        self.assertTrue(service.is_complete(result))
        self.assertEqual(result["Album"], "Astérix")

    def test_complementary_repositories(self):
        """Test avec deux repositories qui se complètent"""
        service = GetInfosService([self.partial_repo_1, self.partial_repo_2])
        result = service.main(123)

        self.assertIsNotNone(result)
        self.assertTrue(service.is_complete(result))
        self.assertEqual(result["Album"], "Astérix")
        self.assertEqual(result["Couleurs"], "Albert Uderzo")
        self.assertEqual(result["Synopsis"], "Les aventures d'Astérix")

    def test_incomplete_repositories(self):
        """Test avec des repositories qui ne peuvent pas compléter toutes les informations"""
        service = GetInfosService([self.partial_repo_1])
        result = service.main(123)

        self.assertIsNotNone(result)
        self.assertFalse(service.is_complete(result))
        self.assertEqual(result["Synopsis"], "")

    def test_incomplete_repositories_on_error(self):
        """Test avec des repositories qui ne peuvent pas compléter toutes les informations dont un en erreur"""
        service = GetInfosService([self.partial_repo_1, self.error_repo])
        result = service.main(123)

        self.assertIsNotNone(result)
        self.assertFalse(service.is_complete(result))
        self.assertEqual(result["Synopsis"], "")

    def test_error_handling(self):
        """Test de la gestion des erreurs"""
        service = GetInfosService([self.empty_repo, self.complete_repo])
        result = service.main(123)

        self.assertIsNotNone(result)
        self.assertTrue(service.is_complete(result))
        self.assertEqual(result["Album"], "Astérix")

    def test_empty_repositories_list(self):
        """Test avec une liste vide de repositories"""
        service = GetInfosService([])
        with self.assertRaises(AddAlbumError):
            service.main(123)

    def test_preserve_first_valid_value(self):
        """Test que les valeurs non vides ne sont pas écrasées"""
        repo1 = BdInMemory("repo1", {"Album": "Premier titre"})
        repo2 = BdInMemory("repo2", {"Album": "Second titre"})

        service = GetInfosService([repo1, repo2])
        result = service.main(123)

        self.assertEqual(result["Album"], "Premier titre")


if __name__ == '__main__':
    unittest.main()
