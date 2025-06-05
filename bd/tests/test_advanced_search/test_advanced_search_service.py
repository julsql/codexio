import os
import sys
import unittest
from unittest.mock import Mock

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tests.test_advanced_search.internal.advanced_search_in_memory import InMemoryAdvancedSearchRepository
from main.core.application.usecases.advanced_search.advanced_search_service import AdvancedSearchService
from main.core.domain.forms.forms import RechercheForm


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
        result = self.service.form_search()

        # Vérifications
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].isbn, 123456789)
        self.assertEqual(result[0].title, "Album Test")
        self.assertEqual(result[0].series, "Série Test")
        self.assertEqual(result[0].number, "1")
        self.assertEqual(result[0].writer, "Auteur Test")
        self.assertEqual(result[0].illustrator, "Illustrateur Test")

    def test_form_search_avec_form_valide(self):
        # Création d'un form avec des données valides
        form = RechercheForm(data={
            'series': 'Série Test',
            'writer': 'Auteur Test'
        })
        self.assertTrue(form.is_valid())

        # Exécution
        result = self.service.form_search(form)

        # Vérifications
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].series, "Série Test")
        self.assertEqual(result[0].writer, "Auteur Test")

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
        result = self.service.main(mock_request)

        # Vérifications
        self.assertIsInstance(result.form, RechercheForm)
        self.assertEqual(len(result.albums), 1)
        self.assertFalse(result.is_form_send)
        self.assertEqual(result.albums[0].isbn, 123456789)

    def test_main_methode_post(self):
        # Création d'une requête POST avec des données de recherche
        mock_request = Mock()
        mock_request.method = 'POST'
        mock_request.POST = {
            'series': 'Série Test'
        }

        # Exécution
        result = self.service.main(mock_request)

        # Vérifications
        self.assertIsInstance(result.form, RechercheForm)
        self.assertEqual(len(result.albums), 1)
        self.assertTrue(result.is_form_send)
        self.assertEqual(result.albums[0].series, "Série Test")

    def test_main_methode_post_sans_resultats(self):
        # Création d'une requête POST avec des données qui ne correspondent à aucune BD
        mock_request = Mock()
        mock_request.method = 'POST'
        mock_request.POST = {
            'series': 'Série Inexistante'
        }

        # Exécution
        result = self.service.main(mock_request)

        # Vérifications
        self.assertIsInstance(result.form, RechercheForm)
        self.assertEqual(len(result.albums), 0)
        self.assertTrue(result.is_form_send)


if __name__ == '__main__':
    unittest.main()
