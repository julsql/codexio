import unittest
from dataclasses import fields
from datetime import date
from decimal import Decimal

from main.core.domain.model.album import Album
from main.core.infrastructure.interface_adapters.views.formatters import album_to_dict


class TestAlbumToDict(unittest.TestCase):
    def test_full_album(self):
        album = Album(
            isbn=9782012101418,
            title="Astérix le Gaulois",
            number="1",
            series="Astérix",
            writer="René Goscinny",
            illustrator="Albert Uderzo",
            colorist="Albert Uderzo",
            publisher="Hachette",
            publication_date=date(1961, 10, 30),
            edition="Hachette",
            number_of_pages=48,
            purchase_price=Decimal("9.99"),
            synopsis="Nous sommes en 50 avant Jésus-Christ",
            image="http://image.jpg",
        )

        result = album_to_dict(album)

        self.assertEqual(result["isbn"], 9782012101418)
        self.assertEqual(result["title"], "Astérix le Gaulois")
        self.assertEqual(result["publication_date"], "1961-10-30")
        self.assertEqual(result["purchase_price"], 9.99)
        self.assertEqual(result["number_of_pages"], 48)

    def test_empty_album(self):
        result = album_to_dict(Album(isbn=1234567890))

        self.assertIsNone(result["publication_date"])
        self.assertIsNone(result["purchase_price"])
        self.assertEqual(result["title"], "")
        self.assertEqual(result["number_of_pages"], 0)

    def test_free_album_keeps_zero_price(self):
        """Un prix nul doit rester 0, pas devenir null (indiscernable d'un prix inconnu)"""
        result = album_to_dict(Album(isbn=1234567890, purchase_price=Decimal("0")))

        self.assertEqual(result["purchase_price"], 0.0)
        self.assertIsNotNone(result["purchase_price"])

    def test_all_album_fields_are_exposed(self):
        """Tout champ ajouté à Album doit être exposé par l'endpoint"""
        result = album_to_dict(Album(isbn=1234567890))

        self.assertEqual(set(result.keys()), {field.name for field in fields(Album)})


if __name__ == "__main__":
    unittest.main()
