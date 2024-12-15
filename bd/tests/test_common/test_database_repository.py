import unittest
from unittest.mock import patch
from main.core.common.database.internal.bd_model import BD
from main.core.common.database.database_repository import DatabaseRepository
from main.core.common.database.internal.database_connexion import DatabaseConnexion


class TestDatabaseRepository(unittest.TestCase):

    @patch.object(DatabaseRepository, 'get_all', return_value=[])  # Mock de la méthode get_all
    @patch.object(BD, 'objects')  # Mock de l'ORM (modèle BD)
    def test_create_table(self, mock_bd_objects, mock_get_all):
        # Créer une instance de la classe à tester
        db_conn = DatabaseConnexion()

        # Mock des méthodes
        mock_bd_objects.all.return_value.delete.return_value = None

        # Appeler la méthode à tester
        db_conn.create_table()

        # Vérifier que la méthode delete a été appelée sur BD.objects.all()
        mock_bd_objects.all.assert_called_once()
        mock_bd_objects.all.return_value.delete.assert_called_once()

    @patch.object(BD.objects, 'bulk_create')  # Mock de la méthode bulk_create de l'ORM
    def test_insert(self, mock_bulk_create):
        # Préparer des données fictives à insérer
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
                "number_of_pages": "100",
                "rating": "5",
                "purchase_price": "20.0",
                "year_of_purchase": "2024",
                "place_of_purchase": "Online",
                "deluxe_edition": "",
                "signed_copy": "",
                "ex_libris": "",
                "synopsis": "A test synopsis.",
                "image": "test_image.png",
            }
        ]

        # Créer une instance de la classe à tester
        db_conn = DatabaseConnexion()

        # Appeler la méthode à tester
        db_conn.insert(values)

        # Vérifier que bulk_create a été appelé avec les bons objets
        mock_bulk_create.assert_called_once()

    @patch.object(BD.objects, 'all')  # Mock de la méthode all de l'ORM
    def test_get_all(self, mock_all):
        # Données simulées que vous attendez de la base de données
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
                "number_of_pages": "100",
                "rating": "5",
                "purchase_price": "20.0",
                "year_of_purchase": "2024",
                "place_of_purchase": "Online",
                "deluxe_edition": "",
                "signed_copy": "",
                "ex_libris": "",
                "synopsis": "A test synopsis.",
                "image": "test_image.png",
            }
        ]

        # Créer une instance de la classe à tester
        db_conn = DatabaseConnexion()

        # Appeler la méthode à tester
        result = db_conn.get_all()

        # Vérifier que la méthode all a été appelée
        mock_all.assert_called_once()

        # Vérifier que le résultat est correct
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['isbn'], "1234567890")
        self.assertEqual(result[0]['album'], "Test Album")

if __name__ == '__main__':
    unittest.main()
