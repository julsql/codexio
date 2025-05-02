import os
import sys
import unittest
from unittest.mock import Mock

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tests.test_advanced_search.internal.advanced_search_in_memory import InMemoryAdvancedSearchRepository
from main.core.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.advanced_search.internal.forms import RechercheForm


class TestAdvancedSearchService(unittest.TestCase):
    def setUp(self):
        # Utilisation du repository en mémoire
        self.repository = InMemoryAdvancedSearchRepository()
        self.service = AdvancedSearchService(self.repository)

        # Ajout d'une BD de test dans le repository
        self.repository.add_bd(
            isbn="123456789",
            album="Album Test",
            number="1",
            series="Série Test",
            writer="Auteur Test",
            illustrator="Illustrateur Test"
        )

    def test_form_search_sans_form(self):
        # Exécution
        resultat = self.service.form_search()

        # Vérifications
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]['ISBN'], "123456789")
        self.assertEqual(resultat[0]['Album'], "Album Test")
        self.assertEqual(resultat[0]['Serie'], "Série Test")
        self.assertEqual(resultat[0]['Numero'], "1")
        self.assertEqual(resultat[0]['Scenariste'], "Auteur Test")
        self.assertEqual(resultat[0]['Dessinateur'], "Illustrateur Test")

    def test_form_search_avec_form_valide(self):
        # Création d'un form avec des données valides
        form = RechercheForm(data={
            'series': 'Série Test',
            'writer': 'Auteur Test'
        })
        self.assertTrue(form.is_valid())

        # Exécution
        resultat = self.service.form_search(form)

        # Vérifications
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0]['Serie'], "Série Test")
        self.assertEqual(resultat[0]['Scenariste'], "Auteur Test")

    def test_form_search_avec_form_sans_resultats(self):
        # Création d'un form avec des données qui ne correspondent à aucune BD
        form = RechercheForm(data={
            'series': 'Série Inexistante'
        })
        self.assertTrue(form.is_valid())

        # Exécution
        resultat = self.service.form_search(form)

        # Vérifications
        self.assertEqual(len(resultat), 0)

    def test_main_methode_get(self):
        # Création d'une requête GET
        mock_request = Mock()
        mock_request.method = 'GET'

        # Exécution
        form, infos, count, is_post = self.service.main(mock_request)

        # Vérifications
        self.assertIsInstance(form, RechercheForm)
        self.assertEqual(len(infos), 1)
        self.assertEqual(count, 1)
        self.assertFalse(is_post)
        self.assertEqual(infos[0]['ISBN'], "123456789")

    def test_main_methode_post(self):
        # Création d'une requête POST avec des données de recherche
        mock_request = Mock()
        mock_request.method = 'POST'
        mock_request.POST = {
            'series': 'Série Test'
        }

        # Exécution
        form, infos, count, is_post = self.service.main(mock_request)

        # Vérifications
        self.assertIsInstance(form, RechercheForm)
        self.assertEqual(len(infos), 1)
        self.assertEqual(count, 1)
        self.assertTrue(is_post)
        self.assertEqual(infos[0]['Serie'], "Série Test")

    def test_main_methode_post_sans_resultats(self):
        # Création d'une requête POST avec des données qui ne correspondent à aucune BD
        mock_request = Mock()
        mock_request.method = 'POST'
        mock_request.POST = {
            'series': 'Série Inexistante'
        }

        # Exécution
        form, infos, count, is_post = self.service.main(mock_request)

        # Vérifications
        self.assertIsInstance(form, RechercheForm)
        self.assertEqual(len(infos), 0)
        self.assertEqual(count, 0)
        self.assertTrue(is_post)


if __name__ == '__main__':
    unittest.main()
