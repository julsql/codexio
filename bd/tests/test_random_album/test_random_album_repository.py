import os
import sys
import unittest
from datetime import date

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.core.common.database.internal.bd_model import BD
from main.core.random_album.internal.random_album_connexion import RandomAlbumConnexion


class TestRandomAlbumConnexion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repository = RandomAlbumConnexion()

    def setUp(self):
        # Nettoyage de la base avant chaque test
        BD.objects.all().delete()

        self.bd1 = {
            'isbn': "123456789",
            'album': "Astérix le Gaulois",
            'number': "1",
            'series': "Astérix",
            'writer': "René Goscinny",
            'illustrator': "Albert Uderzo",
            'image': "asterix.jpg",
            'publication_date': date(1961, 10, 29),
            'purchase_price': 15.0,
            'number_of_pages': 48,
            'edition': "Standard",
            'synopsis': "Les aventures d'Astérix",
            'deluxe_edition': False
        }
        self.bd2 = {
            'isbn': "987654321",
            'album': "Tintin au Tibet",
            'number': "20",
            'series': "Les aventures de Tintin",
            'writer': "Hergé",
            'illustrator': "Hergé",
            'image': "tintin.jpg",
            'publication_date': date(1960, 1, 1),
            'purchase_price': 20.99,
            'number_of_pages': 62,
            'edition': "Deluxe",
            'synopsis': "Tintin part au Tibet",
            'deluxe_edition': False
        }

        # Création de données de test
        BD.objects.create(
            **self.bd1
        )

        BD.objects.create(
            **self.bd2
        )

    def tearDown(self):
        BD.objects.all().delete()

    def test_get_random_album_empty_database(self):
        # Arrange
        BD.objects.all().delete()

        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertIsNone(result)

    def test_get_random_album_returns_dict_with_correct_fields(self):
        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertIsInstance(result, dict)
        expected_fields = {
            'isbn', 'album', 'number', 'series', 'image', 'writer',
            'illustrator', 'publication_date', 'purchase_price',
            'number_of_pages', 'edition', 'synopsis'
        }
        self.assertEqual(expected_fields, set(result.keys()))

    def test_get_random_album_integer_price(self):
        # Arrange
        BD.objects.all().delete()
        BD.objects.create(
            isbn="111111111",
            album="Test Album",
            purchase_price=25.0,
            deluxe_edition=False
        )

        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertEqual(25, result['purchase_price'])

    def test_get_random_album_float_price(self):
        # Arrange
        BD.objects.all().delete()
        BD.objects.create(
            isbn="111111111",
            album="Test Album",
            purchase_price=25.99,
            deluxe_edition=False
        )

        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertEqual(25.99, result['purchase_price'])

    def test_get_random_album_returns_valid_data(self):
        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertIn(str(result['isbn']), ["123456789", "987654321"])
        if str(result['isbn']) == self.bd1['isbn']:
            bd = self.bd1
        else:
            bd = self.bd2

        self.assertEqual(bd['album'], result['album'])
        self.assertEqual(bd['number'], result['number'])
        self.assertEqual(bd['series'], result['series'])
        self.assertEqual(bd['writer'], result['writer'])
        self.assertEqual(bd['illustrator'], result['illustrator'])
        self.assertEqual(bd['image'], result['image'])
        self.assertEqual(bd['publication_date'], result['publication_date'])
        self.assertEqual(bd['purchase_price'], result['purchase_price'])
        self.assertEqual(bd['number_of_pages'], result['number_of_pages'])
        self.assertEqual(bd['edition'], result['edition'])
        self.assertEqual(bd['synopsis'], result['synopsis'])


if __name__ == '__main__':
    unittest.main()
