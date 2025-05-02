import os
import sys
import unittest

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db.models import QuerySet
from main.core.common.database.internal.bd_model import BD
from main.core.advanced_search.internal.advanced_search_connexion import AdvancedSearchConnexion
from datetime import date


class TestAdvancedSearchRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repository = AdvancedSearchConnexion()

    def setUp(self):
        # Nettoyage de la base avant chaque test
        BD.objects.all().delete()

        # Création de données de test
        self.bd1 = BD.objects.create(
            isbn="123456789",
            album="Astérix le Gaulois",
            number="1",
            series="Astérix",
            writer="René Goscinny",
            illustrator="Albert Uderzo",
            publication_date=date(1961, 10, 29),
            synopsis="Les aventures d'Astérix",
            deluxe_edition=False,
        )

        self.bd2 = BD.objects.create(
            isbn="987654321",
            album="Tintin au Tibet",
            number="20",
            series="Tintin",
            writer="Hergé",
            illustrator="Hergé",
            publication_date=date(1960, 1, 1),
            synopsis="Les aventures de Tintin",
            deluxe_edition=False,
        )

    def tearDown(self):
        BD.objects.all().delete()

    def test_get_all(self):
        # Exécution
        result = self.repository.get_all()

        # Vérifications
        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result.count(), 2)
        self.assertIn(self.bd1, result)
        self.assertIn(self.bd2, result)

    def test_get_by_form_with_series(self):
        # Exécution
        result = self.repository.get_by_form(
            {'series': 'Astérix'},
            self.repository.get_all()
        )

        # Vérifications
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.bd1)

    def test_get_by_form_with_multiple_criteria(self):
        # Exécution
        result = self.repository.get_by_form(
            {
                'writer': 'Goscinny',
                'illustrator': 'Uderzo'
            },
            self.repository.get_all()
        )

        # Vérifications
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.bd1)

    def test_get_by_form_with_date_range(self):
        # Exécution
        result = self.repository.get_by_form(
            {
                'start_date': date(1960, 1, 1),
                'end_date': date(1961, 1, 1)
            },
            self.repository.get_all()
        )

        # Vérifications
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.bd2)

    def test_get_by_form_with_synopsis(self):
        # Exécution
        result = self.repository.get_by_form(
            {'synopsis': 'Astérix'},
            self.repository.get_all()
        )

        # Vérifications
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.bd1)

    def test_get_by_form_no_results(self):
        # Exécution
        result = self.repository.get_by_form(
            {'series': 'Série inexistante'},
            self.repository.get_all()
        )

        # Vérifications
        self.assertEqual(result.count(), 0)

    def test_order_by_series_ascending(self):
        # Exécution
        result = self.repository.order_by(
            self.repository.get_all(),
            'series',
            True
        )

        # Vérifications
        bds = list(result)
        self.assertEqual(bds[0], self.bd1)  # Astérix avant Tintin
        self.assertEqual(bds[1], self.bd2)

    def test_order_by_series_descending(self):
        # Exécution
        result = self.repository.order_by(
            self.repository.get_all(),
            'series',
            False
        )

        # Vérifications
        bds = list(result)
        self.assertEqual(bds[0], self.bd2)  # Tintin avant Astérix
        self.assertEqual(bds[1], self.bd1)


if __name__ == '__main__':
    unittest.main()
