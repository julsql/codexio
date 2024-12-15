import unittest
from unittest.mock import patch
from main.core.common.database.internal.bd_model import BD
from main.core.common.database.database_repository import DatabaseRepository
from main.core.common.database.internal.database_connexion import DatabaseConnexion


class TestDatabaseConnexion(unittest.TestCase):

    @patch.object(DatabaseRepository, 'get_all', return_value=[])
    @patch.object(BD, 'objects')
    def test_create_table(self, mock_bd_objects, mock_get_all):
        db_conn = DatabaseConnexion()

        mock_bd_objects.all.return_value.delete.return_value = None

        db_conn.create_table()

        mock_bd_objects.all.assert_called_once()
        mock_bd_objects.all.return_value.delete.assert_called_once()

    @patch.object(BD.objects, 'bulk_create')
    def test_insert(self, mock_bulk_create):
        values = [
            {
                "isbn": "1234567890",
                "album": "Test Album",
                "number": "1",
                "series": "Test Series",
                "writer": "Test Writer",
                "illustrator": "Test Illustrator",
                "colorist": "Test Colorist",
                "publisher": "Test Publisher",
                "publication_date": "2024-12-01",
                "edition": "First",
                "number_of_pages": 100,
                "rating": "5",
                "purchase_price": 20.0,
                "year_of_purchase": 2024,
                "place_of_purchase": "Online",
                "deluxe_edition": False,
                "signed_copy": False,
                "ex_libris": False,
                "synopsis": "A test synopsis.",
                "image": "test_image.png",
            }
        ]

        db_conn = DatabaseConnexion()

        db_conn.insert(values)

        mock_bulk_create.assert_called_once()

    @patch.object(BD.objects, 'all')
    def test_get_all(self, mock_all):
        mock_all.return_value.values.return_value = [
            {
                "isbn": "1234567890",
                "album": "Test Album",
                "number": "1",
                "series": "Test Series",
                "writer": "Test Writer",
                "illustrator": "Test Illustrator",
                "colorist": "Test Colorist",
                "publisher": "Test Publisher",
                "publication_date": "2024-12-01",
                "edition": "First",
                "number_of_pages": 100,
                "rating": "5",
                "purchase_price": 20.0,
                "year_of_purchase": 2024,
                "place_of_purchase": "Online",
                "deluxe_edition": False,
                "signed_copy": False,
                "ex_libris": False,
                "synopsis": "A test synopsis.",
                "image": "test_image.png",
            }
        ]

        db_conn = DatabaseConnexion()

        result = db_conn.get_all()

        mock_all.assert_called_once()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['isbn'], "1234567890")
        self.assertEqual(result[0]['album'], "Test Album")

if __name__ == '__main__':
    unittest.main()
