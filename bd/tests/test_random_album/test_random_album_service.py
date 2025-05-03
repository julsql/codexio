import unittest
from datetime import date

from main.core.random_album.random_album_service import RandomAlbumService
from test_random_album.internal.random_album_in_memory import RandomAlbumInMemory


class TestRandomAlbumService(unittest.TestCase):
    def setUp(self) -> None:
        self.test_album = {
            'isbn': '123456789',
            'album': 'Test Album',
            'number': '1',
            'series': 'Test Series',
            'writer': 'Test Writer',
            'illustrator': 'Test Illustrator',
            'publication_date': date(2024, 1, 1),
            'purchase_price': 15.0,
            'number_of_pages': 48,
            'edition': 'Standard',
            'synopsis': 'Test Synopsis',
            'image': 'test.jpg'
        }

    def test_main_returns_none_when_no_album(self) -> None:
        # Arrange
        repository = RandomAlbumInMemory(None)
        service = RandomAlbumService(repository)

        # Act
        result = service.main()

        # Assert
        self.assertIsNone(result)
        self.assertTrue(repository.get_random_album_called)

    def test_main_returns_album_when_exists(self) -> None:
        # Arrange
        repository = RandomAlbumInMemory([self.test_album])
        service = RandomAlbumService(repository)

        # Act
        result = service.main()

        # Assert
        self.assertEqual(self.test_album, result)
        self.assertTrue(repository.get_random_album_called)
        self.assertEqual(self.test_album['isbn'], result['isbn'])
        self.assertEqual(self.test_album['album'], result['album'])
        self.assertEqual(self.test_album['series'], result['series'])
        self.assertEqual(self.test_album['writer'], result['writer'])
        self.assertEqual(self.test_album['illustrator'], result['illustrator'])
        self.assertEqual(self.test_album['publication_date'], result['publication_date'])
        self.assertEqual(self.test_album['purchase_price'], result['purchase_price'])
        self.assertEqual(self.test_album['number_of_pages'], result['number_of_pages'])
        self.assertEqual(self.test_album['edition'], result['edition'])
        self.assertEqual(self.test_album['synopsis'], result['synopsis'])
        self.assertEqual(self.test_album['image'], result['image'])


if __name__ == '__main__':
    unittest.main()
