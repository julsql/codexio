import unittest
from datetime import date
from decimal import Decimal

from main.application.usecases.random_album.random_album_service import RandomAlbumService
from main.domain.model.album import Album
from test_random_album.internal.random_album_in_memory import RandomAlbumInMemory


class TestRandomAlbumService(unittest.TestCase):
    def setUp(self) -> None:
        self.test_album = Album(
            isbn=123456789,
            titre='Test Album',
            numero='1',
            serie='Test Series',
            scenariste='Test Writer',
            dessinateur='Test Illustrator',
            date_publication=date(2024, 1, 1),
            prix=Decimal("15.0"),
            nombre_pages=48,
            edition='Standard',
            synopsis='Test Synopsis',
            image_url='test.jpg'
        )

    def test_main_returns_none_when_no_album(self) -> None:
        # Arrange
        repository = RandomAlbumInMemory([Album(0)])
        service = RandomAlbumService(repository)

        # Act
        result = service.main()

        # Assert
        self.assertTrue(result.is_empty())
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
        self.assertEqual(self.test_album, result)


if __name__ == '__main__':
    unittest.main()
