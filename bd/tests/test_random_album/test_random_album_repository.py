import os
import sys
import unittest
from datetime import date

import django

from main.domain.model.album import Album

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from main.infrastructure.persistence.database.models import BD
from main.infrastructure.persistence.database.random_album_adapter import RandomAlbumAdapter


class TestRandomAlbumConnexion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.repository = RandomAlbumAdapter()

    def setUp(self):
        # Nettoyage de la base avant chaque test
        BD.objects.all().delete()

        self.bd1 = {
            'isbn': 123456789,
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
            'isbn': 987654321,
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
        self.assertTrue(result.is_empty())

    def test_get_random_album_returns_dict_with_correct_fields(self):
        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertIsInstance(result, Album)

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
        self.assertEqual(25, result.prix)

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
        self.assertEqual(25.99, float(result.prix))

    def test_get_random_album_returns_valid_data(self):
        # Act
        result = self.repository.get_random_album()

        # Assert
        self.assertIn(result.isbn, [123456789, 987654321])
        if result.isbn == self.bd1['isbn']:
            bd = self.bd1
        else:
            bd = self.bd2

        self.assertEqual(bd['album'], result.titre)
        self.assertEqual(bd['number'], result.numero)
        self.assertEqual(bd['series'], result.serie)
        self.assertEqual(bd['writer'], result.scenariste)
        self.assertEqual(bd['illustrator'], result.dessinateur)
        self.assertEqual(bd['image'], result.image_url)
        self.assertEqual(bd['publication_date'], result.date_publication)
        self.assertEqual(bd['purchase_price'], float(result.prix))
        self.assertEqual(bd['number_of_pages'], result.nombre_pages)
        self.assertEqual(bd['edition'], result.edition)
        self.assertEqual(bd['synopsis'], result.synopsis)


if __name__ == '__main__':
    unittest.main()
