import os
import sys
import unittest
from datetime import date

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db.models import QuerySet

from main.core.infrastructure.persistence.database.advanced_search_adapter import AdvancedSearchAdapter
from main.core.infrastructure.persistence.database.models.bd import BD


class TestAdvancedSearchRepository(unittest.TestCase):
    EMPTY = 0

    @classmethod
    def setUpClass(cls):
        cls.repository = AdvancedSearchAdapter()

    def setUp(self):
        # Nettoyage de la base avant chaque test
        BD.objects.all().delete()

        # Création de données de test plus complètes
        self.bd1 = BD.objects.create(
            isbn="123456789",
            album="Astérix le Gaulois",
            number="1",
            series="Astérix",
            writer="René Goscinny",
            illustrator="Albert Uderzo",
            publisher="Dargaud",
            edition="Standard",
            publication_date=date(1961, 10, 29),
            synopsis="Les aventures d'Astérix, un guerrier gaulois rusé, et son ami Obélix",
            deluxe_edition=False,
            year_of_purchase=2020
        )

        self.bd2 = BD.objects.create(
            isbn="987654321",
            album="Tintin au Tibet",
            number="20",
            series="Les aventures de Tintin",
            writer="Hergé",
            illustrator="Hergé",
            publisher="Casterman",
            edition="Deluxe",
            publication_date=date(1960, 1, 1),
            synopsis="Tintin part au Tibet à la recherche de son ami Tchang pour des grandes aventures",
            deluxe_edition=True,
            year_of_purchase=2021
        )

        self.total_row = 2

    def tearDown(self):
        BD.objects.all().delete()

    def test_get_all(self):
        result = self.repository.get_all()
        self.assertIsInstance(result, QuerySet)
        self.assertEqual(self.total_row, result.count())
        self.assertIn(self.bd1, result)
        self.assertIn(self.bd2, result)

    def test_filter_contains_case_diacritique_insensitive(self):
        result = self.repository.get_by_form(
            {'series': 'asterix'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd1, result.first())

    def test_filter_contains_partial_match(self):
        result = self.repository.get_by_form(
            {'album': 'Gaulois'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd1, result.first())

    def test_filter_contains_multiple_words(self):
        result = self.repository.get_by_form(
            {'album': 'aventures Tintin Tibet'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_filter_equals_exact_match(self):
        result = self.repository.get_by_form(
            {'isbn': '123456789'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd1, result.first())

    def test_filter_date_range_inclusive(self):
        result = self.repository.get_by_form(
            {
                'start_date': date(1960, 1, 1),
                'end_date': date(1961, 12, 31)
            },
            self.repository.get_all()
        )
        self.assertEqual(self.total_row, result.count())

    def test_filter_date_start_only(self):
        result = self.repository.get_by_form(
            {'start_date': date(1961, 1, 1)},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd1, result.first())

    def test_filter_date_end_only(self):
        result = self.repository.get_by_form(
            {'end_date': date(1960, 12, 31)},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_search_synopsis_only_stop_words_returns_empty(self):
        """Test que la recherche avec uniquement des mots vides renvoie un queryset vide"""
        result = self.repository.get_by_form(
            {'synopsis': 'le et au de'},
            self.repository.get_all()
        )
        self.assertEqual(self.EMPTY, result.count())

    def test_search_synopsis_short_words_returns_empty(self):
        """Test que la recherche avec uniquement des mots courts renvoie un queryset vide"""
        result = self.repository.get_by_form(
            {'synopsis': 'il va du'},
            self.repository.get_all()
        )
        self.assertEqual(self.EMPTY, result.count())

    def test_search_synopsis_only_stop_words_returns_empty(self):
        """Test que la recherche avec uniquement des mots exclus renvoie un résultat"""
        result = self.repository.get_by_form(
            {'synopsis': 'un son'},
            self.repository.get_all()
        )
        self.assertEqual(self.total_row, result.count())

    def test_search_synopsis_mixed_words(self):
        """Test que la recherche fonctionne avec un mélange de mots vides et significatifs"""
        result = self.repository.get_by_form(
            {'synopsis': 'l\'aventure de Tintin'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_search_synopsis_with_accents(self):
        """Test que la recherche est insensible aux accents"""
        result = self.repository.get_by_form(
            {'synopsis': 'asterix'},  # Sans accent
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd1, result.first())

    def test_search_synopsis_with_case_sensitivity(self):
        """Test que la recherche est insensible à la casse"""
        result = self.repository.get_by_form(
            {'synopsis': 'TINTIN'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_search_synopsis_partial_word(self):
        """Test que la recherche fonctionne avec des mots partiels"""
        result = self.repository.get_by_form(
            {'synopsis': 'aventur'},  # Devrait matcher 'aventures'
            self.repository.get_all()
        )
        self.assertEqual(self.total_row, result.count())

    def test_search_synopsis_multiple_words_all_must_match(self):
        """Test que tous les mots de recherche doivent être présents"""
        result = self.repository.get_by_form(
            {'synopsis': 'Tintin Tibet recherche'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_search_synopsis_empty_string(self):
        """Test avec une chaîne vide"""
        result = self.repository.get_by_form(
            {'synopsis': ''},
            self.repository.get_all()
        )
        self.assertEqual(self.total_row, result.count())

    def test_search_synopsis_whitespace_only(self):
        """Test avec uniquement des espaces"""
        result = self.repository.get_by_form(
            {'synopsis': '   '},
            self.repository.get_all()
        )
        self.assertEqual(self.total_row, result.count())

    def test_search_synopsis_special_characters(self):
        """Test avec des caractères spéciaux"""
        result = self.repository.get_by_form(
            {'synopsis': 'recherche!@#$%^&*()'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_search_synopsis_significant_stop_words(self):
        """Test avec des mots qui sont normalement des stop words mais significatifs dans le contexte"""
        # Ajoutons une BD avec un mot stop dans le synopsis
        bd3 = BD.objects.create(
            isbn="555555555",
            album="Test",
            synopsis="Cette BD parle de puis et donc",
            deluxe_edition=False
        )

        result = self.repository.get_by_form(
            {'synopsis': 'puis donc'},  # Ces mots sont dans STOP_WORDS
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(bd3, result.first())

    def test_search_synopsis_accents(self):
        result = self.repository.get_by_form(
            {'synopsis': 'asterix et son ami'},
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd1, result.first())

    def test_multiple_criteria_combined(self):
        result = self.repository.get_by_form(
            {
                'writer': 'Hergé',
                'deluxe_edition': True,
                'publisher': 'Casterman'
            },
            self.repository.get_all()
        )
        self.assertEqual(1, result.count())
        self.assertEqual(self.bd2, result.first())

    def test_empty_form_returns_all(self):
        result = self.repository.get_by_form(
            {},
            self.repository.get_all()
        )
        self.assertEqual(self.total_row, result.count())


if __name__ == '__main__':
    unittest.main()
