import unittest
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

    def test_all_keys_present(self):
        result = album_to_dict(Album(isbn=1234567890))

        expected_keys = {
            "isbn", "title", "number", "series", "writer", "illustrator", "translator",
            "colorist", "publisher", "collection_book", "literary_genre", "style",
            "origin_language", "publication_date", "edition", "number_of_pages",
            "purchase_price", "synopsis", "image",
        }
        self.assertEqual(set(result.keys()), expected_keys)


if __name__ == "__main__":
    unittest.main()
